#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from monitorbin.util.process import ProcessCL

# author: cg错过
# time: 2017-12-06

class Pm2Operate:

    def __init__(self, fileUtilObj, dataTempObj, intHourTime, intHourCheckAll, allModuleRunAllObj):

        # intDateMin: 当前运行脚本的分钟数
        # intMintHour: 配置文件中设置的时间(分钟数)
        # fileUtilObj: FileUtil的对象(脚本从运行到结束都只有这一个FileUtil对象)

        self.intHourTime = intHourTime
        self.intHourCheckAll = intHourCheckAll
        self.fileUtilObj = fileUtilObj
        self.dataTempObj = dataTempObj
        self.allModuleRunAllObj = allModuleRunAllObj

        self.checkPm2()


    def checkPm2(self):

        if((self.intHourTime == self.intHourCheckAll) or (self.intHourTime == ("0" + self.intHourCheckAll))):

            if(self.allModuleRunAllObj.intOverAllCheckPm2 == 0):
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("-->准备检测pm2", 'runLog')
                self.checkTog()
                self.allModuleRunAllObj.intOverAllCheckPm2 = 1
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("今日检测pm2次数已标记为" +
                                                   str(self.allModuleRunAllObj.intOverAllCheckPm2)), 'runLog')
            else:
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("今日" + str(self.intHourCheckAll) +
                                                "内已检测pm2,今日将不再全面检测\n" +
                                                 "将进行错误监控任务"), 'runLog')
                

    def checkTog(self):
        
        strPm2Status = self.getPm2List()
        
        if(self.fileUtilObj.boolWhetherShowLog & True):
            self.fileUtilObj.writerContent("pm2 list命令输出如下:", 'runLog')
            self.fileUtilObj.writerContent(strPm2Status, 'runLog')
            
        if(strPm2Status.find('stop') != -1):
            self.dataTempObj.dataAll += ("> - pm2容器中有项目未运行\n")
            if(self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("pm2容器中有项目未运行", 'runLog')
                
        else:
            self.dataTempObj.dataAll += ("> - pm2搭载的项目运行正常\n")
            if(self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("pm2搭载的项目运行正常", 'runLog')
        


    def getPm2List(self):

        # 获取pm2 已搭载的项目的状态
        # 运行命令"pm2 list"
        # 返回一个字符串类型的结果

        strPm2List = "pm2 list"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(strPm2List)
        strPm2Status = dictResult.get('stdout')
        return strPm2Status

    '''
    def getRunProjectNum(self):

        #获取搭载的项目的个数
        #返回一个int类型整数

    '''
        
        

        

        
        
