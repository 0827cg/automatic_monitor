#!/usr/bin/python3
#coding=utf-8

from monitorbin.util.process import ProcessCL

#author: cg错过
#time: 2017-09-30

class NginxOperate:

    #nginx检测模块

    def __init__(self, strNginxPath, intDateMin, intMintHour, fileUtilObj):
        
        #strNginxPath: nginx的安装目录
        #intDateMin: 当前运行脚本的分钟数
        #intMintHour: 配置文件中设置的时间(分钟数)
        #fileUtilObj: FileUtil的对象(脚本从运行到结束都只有这一个FileUtil对象)
            
        
        self.fileUtil = fileUtilObj
        self.intDateMin = intDateMin
        self.intMintHour = intMintHour
        self.strNginxPath = strNginxPath
        
        if(self.fileUtil.boolWhetherShowLog & True):
            self.fileUtil.writerContent("-->准备检测nginx", 'runLog')
            self.fileUtil.writerContent("检测nginx路径...", 'runLog')
        
        intCheckResult = self.fileUtil.checkFileExists(self.strNginxPath)
        if(intCheckResult == 1):
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("nginx路径存在,将执行检测nginx", 'runLog')
            self.checkNginx()
        else:
            self.fileUtil.writerContent("配置的nginx路径不存在", 'runLog')
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("nginx检测模块将退出", 'runLog')

    def checkNginx(self):

        #每个小时检测一遍，不做操作
        #其他时候，当检测到未运行时，脚本尝试自启一次

        strNginxStatus = self.getNginxStatus()

        if(self.intDateMin == self.intMintHour):
            self.checkNginxStatus(strNginxStatus)
        else:
             intMark = self.checkNginxStatus(strNginxStatus, 'Second')
             if(intMark == -1):
                 self.tryStartNginx(self.strNginxPath)



    def getNginxStatus(self):
        
        #获取进程中的nginx
        
        nginxStatusCL = "ps -ef | grep nginx"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(nginxStatusCL)
        strNginxStatus = dictResult.get('stdout')
        return strNginxStatus


    def checkNginxStatus(self, strNginxStatus, strFileMark='Hour'):

        #判断nginx是否运行

        intMark = -1
        strNginx = "nginx:"
        
        if(strNginxStatus.find(strNginx) != -1):
            #print("nginx在运行")
            intMark = 1
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("nginx在运行")
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent("nginx在运行", 'runLog')
        else:
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("nginx未运行")
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent("nginx未运行", 'runLog')
            else:
                self.fileUtil.writerContent("nginx未运行", 'Second')
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent("nginx未运行", 'runLog')
            #print("nginx未运行")
        return intMark


    def tryStartNginx(self, strNginxPath):

        #脚本启动nginx

        intMark = -1
        self.fileUtil.writerContent("脚本尝试将其启动...", 'Second')
        if(self.fileUtil.boolWhetherShowLog & True):
            self.fileUtil.writerContent("脚本尝试将其启动...", 'runLog')
        strStartNginxCL = strNginxPath + "/sbin/./nginx"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(strStartNginxCL)
        strErr = dictResult.get('stderr')
        if(strErr == ''):
            #print("nginx已被脚本启动")
            self.fileUtil.writerContent("nginx已被脚本启动", 'Second')
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("nginx已被脚本启动", 'runLog')
            intMark = 1
        else:
            #print("脚本启动nginx未成功，请手动启动")
            self.fileUtil.writerContent("脚本启动nginx未成功，请手动启动", 'Second')
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("脚本启动nginx未成功，请手动启动", 'runLog')
            self.fileUtil.writerErr(("nginx: " + strErr), 'Second')
            #print(strErr)
        return intMark
        
