#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg错过
# time  : 2017-12-27

from monitorbin.util.sysTime import RunTime
from monitorbin.util.process import ProcessCL

class RMlog:

    # 删除自身产生的日志文件模块
    # 配置文件中可以进行配置
    # 其中有rm_log_passday,表示删除多少天以前的
    # when_time_rm: 表示一天中的那个时候开始执行删除任务，按小时

    def __init__(self, fileUtilObj, dictNeedRunMsg):

        self.fileUtilObj = fileUtilObj
        self.intHourTime = int(fileUtilObj.strHourTime)
        self.strLogPath = dictNeedRunMsg.get('logpath')

        dictMsgForRMlog = self.getMsgForRMlog(dictNeedRunMsg)

        self.checkTog(dictMsgForRMlog)
            


    def checkTog(self, dictMsgForRMlog):

        if(self.fileUtilObj.boolWhetherShowLog & True):
            self.fileUtilObj.writerContent("-->尝试准备删除日志文件", 'runLog')

        if((len(dictMsgForRMlog) == 1) and ('err' in dictMsgForRMlog)):
            if(self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("删除日志的配置数据不全,致任务中止", 'runLog')
        else:

            intRMlogHour = int(dictMsgForRMlog.get('when_time_rm'))
            intPassday = int(dictMsgForRMlog.get('rm_log_passday'))

            runTime = RunTime()
            strOtherDay = str(runTime.getPastDataDay(intPassday))
            strNewOtherDay = runTime.doCutHorizontalLine(strOtherDay)

            if((self.intHourTime == intRMlogHour) or (self.intHourTime == int("0" + str(intRMlogHour)))):
            
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("时间已为" + str(intRMlogHour) +
                                                    "时,将准备删除日志文件"), 'runLog')

                listFileName = self.fileUtilObj.getFileNameFromPath(self.strLogPath)
                listNeedRMFileName = self.getNeedRMFileName(listFileName, strNewOtherDay)

                if(len(listNeedRMFileName) != 0):

                    if(self.fileUtilObj.boolWhetherShowLog & True):
                        self.fileUtilObj.writerContent(("需要删除的日志文件有:\n" +
                                                       str(listNeedRMFileName)), 'runLog')
                
                    intMark = self.rmLog(listNeedRMFileName)
                    if(intMark == 1):
                        if(self.fileUtilObj.boolWhetherShowLog & True):
                            self.fileUtilObj.writerContent((str(intPassday) + "天前(" + strOtherDay +
                                                            "之前)的日志文件已都删除"), 'runLog')
                    else:
                        if(self.fileUtilObj.boolWhetherShowLog & True):
                            self.fileUtilObj.writerContent("删除日志出现错误,删除日志任务退出...", 'runLog')
                    
                else:
                    if(self.fileUtilObj.boolWhetherShowLog & True):
                        self.fileUtilObj.writerContent(("未发现" + str(intPassday) + "天前(" + strOtherDay +
                                                       "之前)的日志文件,即无文件需要删除.\n" +
                                                        "删除日志文件任务将退出"), 'runLog')
    
                    
            else:
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("时间不为" + str(intRMlogHour) +
                                                    "时,不执行删除日志文件"), 'runLog')
            
    def getNeedRMFileName(self, listFileName, strNewOtherDay):

        # listFileName: 日志目录下的所有文件名
        # strNewOtherDay: 过去intPassday天的日期,格式已转换成"%Y%m%d"的
        # 其中runTime.getPastDataDay()返回的日期格式时"%Y-%m-%d"
        # 而日志文件的日期格式是"%Y%m%d"
        # 调用runTime中的doCutHorizontalLine()即可将'-'去除
        # 通过字符串的str[xx:xx]来获取日期
        # 例如日志名为: monitor_log-20171215.log
        # 则通过monitor_log-20171215.log[12:20]即可获得20171215
        # 返回需要删除的日志文件名

        listNeedRMFileName = []

        for listFileNameItem in listFileName:

            intFileData = int(listFileNameItem[12:20])
            if(intFileData < int(strNewOtherDay)):
                listNeedRMFileName.append(listFileNameItem)
        
        return listNeedRMFileName



    def rmLog(self, listNeedRMFileName):
        
        # listNeedRMFileName: 需要删除的日志文件名
        # 执行删除
        # 方法若返回1表示已经全部删除成功
        # 返回-1表示全部删除失败

        intMark = 0

        processCL = ProcessCL()

        for listNeedRMFileNameItem in listNeedRMFileName:

            strRMFileCL = ("rm " + (self.strLogPath + "/" + listNeedRMFileNameItem))
            dictResult = processCL.getResultAndProcess(strRMFileCL)
            if(dictResult['stderr'] == ''):
                
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("日志文件" + listNeedRMFileNameItem +
                                                    "已成功删除"), 'runLog')
                intMark = 1
            else:

                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("删除日志" + listNeedRMFileNameItem + \
                                                    "出错,将停止所有删除日志任务"), 'runLog')
                intMark = -1
                break
        
        return intMark         

        

    def getMsgForRMlog(self, dictNeedRunMsg):

        # 获取并检测用以删除日志文件的数据，并判断是否完全
        # 返回一个dict类型的数据
        # rm_log_passday: 删除过去多少天前的日志
        # when_time_rm: 24小时内开始删除日志的时间小时

        dictMsgForRMlog = {}
        for keyItem in dictNeedRunMsg:

            if((keyItem == 'rm_log_passday') | (keyItem == 'when_time_rm')):
                if(dictNeedRunMsg.get(keyItem) != ''):
                    dictMsgForRMlog[keyItem] = dictNeedRunMsg.get(keyItem)
                else:
                    dictMsgForRMlog.clear()
                    dictMsgForRMlog['err'] = "Msg Incomplete"
                    break
        return dictMsgForRMlog
