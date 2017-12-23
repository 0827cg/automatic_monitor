# -*- coding: utf-8 -*-

from monitorbin.util.process import ProcessCL

#author: cg错过
#time: 2017-09-30

class NginxOperate:

    intOverAllCheckNum = 0

    #nginx检测模块

    def __init__(self, strNginxPath, intHourTime, intHourCheckAll, fileUtilObj, allModuleRunAllObj):
        
        #strNginxPath: nginx的安装目录
        #intHourTime: 当前运行脚本的小时数
        #intHourCheckAll: 配置文件中设置的时间(小时数)
        #fileUtilObj: FileUtil的对象(脚本从运行到结束都只有这一个FileUtil对象)

        #2017-12-08将分钟数改为小时，即每天大检测只执行一次
            
        
        self.fileUtil = fileUtilObj
        self.intHourTime = intHourTime
        self.intHourCheckAll = intHourCheckAll
        self.strNginxPath = strNginxPath
        self.allModuleRunAllObj = allModuleRunAllObj
        
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

        if((self.intHourTime == self.intHourCheckAll) or (self.intHourTime == ("0" + self.intHourCheckAll))):

            if(self.allModuleRunAllObj.intOverAllCheckNginxNum == 0):
                
                self.checkNginxStatus(strNginxStatus)
                
                self.allModuleRunAllObj.intOverAllCheckNginxNum = 1
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("今日检测nginx次数已标记为" +
                                                str(self.allModuleRunAllObj.intOverAllCheckNginxNum)), 'runLog')
                
            else:
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("今日" + str(self.intHourCheckAll) +
                                                "内已检测nginx,今日将不再检测\n" +
                                                 "将进行错误监控任务"), 'runLog')
                self.checkTog(strNginxStatus)
                
        else:
            self.checkTog(strNginxStatus)
            '''
             intMark = self.checkNginxStatus(strNginxStatus, 'Second')
             if(intMark == -1):
                 self.tryStartNginx(self.strNginxPath)
            '''

    def checkTog(self, strNginxStatus):

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
        
