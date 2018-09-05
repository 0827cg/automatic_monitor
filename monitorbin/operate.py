#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from monitorbin.util.fileUtil import FileUtil
from monitorbin.module.tomcatCheck import TomcatOperate
from monitorbin.module.nginxCheck import NginxOperate
from monitorbin.module.redisCheck import RedisOperate
from monitorbin.module.diskCheck import DiskSizeCheck
from monitorbin.module.letterCheck import CheckLetter
from monitorbin.module.pm2Check import Pm2Operate
from monitorbin.otherModule.picArrivals import PicArrivals
from monitorbin.otherModule.rmLog import RMlog
from monitorbin.otherModule.countPicNum import CountPicNum
from monitorbin.otherModule.integralSituation import IntegralSit
from monitorbin.util.emailUtil import EmailUtil
from monitorbin.util.dingTalk import ResponseDD
from monitorbin.util.dataTemplate import DataTemplate
from monitorbin.util.allRunNum import AllModuleRunAll
from monitorbin.util.sysTime import RunTime
from threading import Timer
import time

# author: cg错过
# time  : 2017-09-30

class Operate:

    # 选择执行操作类

    def __init__(self):

        self.timingRun()

        '''
        
        self.fileUtil = FileUtil()
     
        self.dictNeedRunMsg = self.fileUtil.getNeedRunMsg()
        
        
        if(len(self.dictNeedRunMsg) > 1):
            self.timingRun()
            #self.runProcess(dictNeedRunMsg)
            #emailUtil = EmailUtil(dictNeedRunMsg, self.fileUtil)
        elif(len(dictNeedRunMsg) == 1):
            self.fileUtil.writerContent("配置文件参数值不全", 'runErr')
        else:
            self.fileUtil.writerContent("配置文件读取失败", 'runErr')

        '''

    def timingRun(self):

        # 这个属于定时器
        # 即定时执行，代码中每个多少秒来执行此方法中的代码
        # 现在代码中实现的是，每间隔相应秒数就会重新实例化一个FileUtil对象，
        # 也就是每间隔相应秒数后将重新读取配置，并写读取系统时间
        # 这一点不足的就是每次执行检测都需要重新读取检测配置文件，这固然好点
        # 但也有不足就是读取浪费，
        # 现在有个想法就是将读取系统时间和读取检测配置文件这两个功能分开来实现
        # 即做到每间隔相应秒数后就读取系统时间，而做到只读取一次配置文件

        self.allModuleRunAll = AllModuleRunAll()

        while True:
            
            self.fileUtil = FileUtil()
            dictNeedRunMsg = self.fileUtil.getNeedRunMsg()
            self.strServerName = dictNeedRunMsg.get('servername')
            self.dataTemplate = DataTemplate(self.fileUtil.strDateTime, self.strServerName)
            # dictNeedRunMsg = self.fileUtil.getNeedRunMsg()
            intRunIntervals = int(dictNeedRunMsg.get('run_intervals'))

            self.intHourCheckAll = dictNeedRunMsg.get('when_hour_checkall')
            self.warningLevel = dictNeedRunMsg.get('warning_level')

            intTimeB = int(dictNeedRunMsg.get('time_beginning'))
            intTimeE = int(dictNeedRunMsg.get('time_end'))
            
            if len(dictNeedRunMsg) > 1:
                
                # 脚本执行检测需要监控的项目

                self.runProcess(dictNeedRunMsg)
                
                #emailUtil = EmailUtil(dictNeedRunMsg, self.fileUtil)
                
            elif len(dictNeedRunMsg) == 1:
                self.fileUtil.writerContent("配置文件参数值不全,未执行检测", 'runLog')
            else:
                self.fileUtil.writerContent("配置文件读取失败,未执行检测", 'runLog')

            # if intTimeB <= int(self.fileUtil.strHourTime) < intTimeE:

            if (int(self.fileUtil.strHourTime) >= intTimeB) and (int(self.fileUtil.strHourTime) <= intTimeE):
                self.choiceSendMsgMethod(dictNeedRunMsg)
            else:
                if self.fileUtil.boolWhetherShowLog & True:
                    self.fileUtil.writerContent("不在时间段内, 不执行发送消息任务", 'runLog')

            if self.fileUtil.boolWhetherShowLog & True:
                self.fileUtil.writerContent((str(intRunIntervals/60) + "分钟后将再次检测运行"), 'runLog')
                self.fileUtil.writerContent("============" + str(RunTime().getDateTime()) + "============", 'runLog')

            time.sleep(intRunIntervals)
            
            if str(self.fileUtil.strHourTime) == "00":
                intIndex = self.allModuleRunAll.initAllNum()
                if intIndex == 1:
                    if self.fileUtil.boolWhetherShowLog & True:
                        self.fileUtil.writerContent("所有项目一天执行次数现已重置为0", 'runLog')
                        self.fileUtil.writerContent("---" + self.fileUtil.strDateTime, 'runLog')
                

        '''    
        timeingObject = Timer(int(intRunIntervals), self.timingRun)
        timeingObject.start()
        '''


    def runProcess(self, dictNeedRunMsg):

        # 运行检测各个项目
        # dictNeedRunMsg: 需要运行的数据项目
        
        listKeys = dictNeedRunMsg.keys()
        for keyItem in listKeys:
            if keyItem.find('tomcat') != -1:
                strTomcatPath = dictNeedRunMsg.get(keyItem)
                tomcatOperate = TomcatOperate(strTomcatPath, self.fileUtil.strHourTime, self.intHourCheckAll,
                                              self.fileUtil, self.allModuleRunAll)
                #print(strTomcatPath)
            if keyItem.find('nginx') != -1:
                strNginxPath = dictNeedRunMsg.get(keyItem)
                nginxOperate = NginxOperate(strNginxPath, self.fileUtil.strHourTime, self.intHourCheckAll,
                                            self.fileUtil, self.allModuleRunAll)
                #print(strNginxPath)
            if keyItem.find('redis') != -1:
                strRedisPath = dictNeedRunMsg.get(keyItem)
                redisOperate = RedisOperate(strRedisPath, self.fileUtil.strHourTime, self.intHourCheckAll,
                                            self.fileUtil, self.allModuleRunAll)
                #print(strRedisPath)
            if keyItem.find('checkdisk') != -1:
                strCheckDisk = dictNeedRunMsg.get(keyItem)
                if(strCheckDisk == 'yes'):
                    diskCheck = DiskSizeCheck(self.fileUtil, self.dataTemplate, dictNeedRunMsg,
                                              self.fileUtil.strHourTime, self.intHourCheckAll, self.warningLevel,
                                              self.allModuleRunAll)
            if keyItem.find('whether_check_letter') != -1:
                strCheckLetter = dictNeedRunMsg.get(keyItem)
                if(strCheckLetter == 'yes'):
                    checkLetter = CheckLetter(self.fileUtil, self.dataTemplate, dictNeedRunMsg,
                                              self.fileUtil.strHourTime, self.intHourCheckAll, self.allModuleRunAll)
            if(keyItem.find('whether_check_pic') != -1):
                strCheckPic = dictNeedRunMsg.get(keyItem)
                if strCheckPic == 'yes':
                    picArrivals = PicArrivals(self.fileUtil, dictNeedRunMsg, self.dataTemplate,
                                              self.fileUtil.strHourTime, self.intHourCheckAll, self.allModuleRunAll)
            if keyItem.find('whether_check_pm2') != -1:
                strCheckPm2 = dictNeedRunMsg.get(keyItem)
                if strCheckPm2 == 'yes':
                    pm2Operate = Pm2Operate(self.fileUtil, self.dataTemplate, self.fileUtil.strHourTime,
                                            self.intHourCheckAll, self.allModuleRunAll)

            if keyItem.find('whether_run_count_num') != -1:
                strWhetherRun = dictNeedRunMsg.get(keyItem)
                if strWhetherRun == 'yes':
                    countPicNum = CountPicNum(self.fileUtil, self.dataTemplate, dictNeedRunMsg, self.fileUtil.strHourTime,
                                              self.intHourCheckAll, self.allModuleRunAll)

            if keyItem.find('whether_get_integral_sit') != -1:
                strWhetherRunIntegral = dictNeedRunMsg.get(keyItem)
                if strWhetherRunIntegral == 'yes':
                    integralSit = IntegralSit(self.fileUtil, self.dataTemplate, dictNeedRunMsg, self.fileUtil.strHourTime,
                                              self.intHourCheckAll, self.allModuleRunAll)

            if keyItem.find('whether_rm_log') != -1:
                strRMlog = dictNeedRunMsg.get(keyItem)
                if strRMlog == 'yes':
                    rmLog = RMlog(self.fileUtil, dictNeedRunMsg)
                    
                    


    def choiceSendMsgMethod(self, dictNeedRunMsg):

        # 根据配置文件来选择使用email或者dingtalk来发送消息

        if 'email' in dictNeedRunMsg:
            if dictNeedRunMsg.get('email') == 'yes':
                EmailUtil(dictNeedRunMsg, self.fileUtil, self.dataTemplate)
            else:
                if self.fileUtil.boolWhetherShowLog & True:
                    self.fileUtil.writerContent("不执行email服务", 'runLog')
        else:
            if self.fileUtil.boolWhetherShowLog & True:
                self.fileUtil.writerContent("不执行email服务", 'runLog')

        if 'dingtalk' in dictNeedRunMsg:
            if dictNeedRunMsg.get('dingtalk') == 'yes':
                ResponseDD(self.fileUtil, self.dataTemplate, dictNeedRunMsg)
            else:
                if self.fileUtil.boolWhetherShowLog & True:
                    self.fileUtil.writerContent("不执行钉钉服务", 'runLog')
        else:
            if self.fileUtil.boolWhetherShowLog & True:
                self.fileUtil.writerContent("不执行钉钉服务", 'runLog')    

