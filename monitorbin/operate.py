#!/usr/bin/python3
#coding=utf-8

from monitorbin.util.fileUtil import FileUtil
from monitorbin.module.tomcatCheck import TomcatOperate
from monitorbin.module.nginxCheck import NginxOperate
from monitorbin.module.redisCheck import RedisOperate
from monitorbin.util.emailUtil import EmailUtil
from threading import Timer

#author: cg错过
#time: 2017-09-30

class Operate:

    #选择执行操作类

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

        #这个属于定时器
        #即定时执行，代码中每个多少秒来执行此方法中的代码
        #现在代码中实现的是，每间隔相应秒数就会重新实例化一个FileUtil对象，
        #也就是每间隔相应秒数后将重新读取配置，并写读取系统时间
        #这一点不足的就是每次执行检测都需要重新读取检测配置文件，这固然好点
        #但也有不足就是读取浪费，
        #现在有个想法就是将读取系统时间和读取检测配置文件这两个功能分开来实现
        #即做到每间隔相应秒数后就读取系统时间，而做到只读取一次配置文件
        
        self.fileUtil = FileUtil()
     
        dictNeedRunMsg = self.fileUtil.getNeedRunMsg()
        intRunIntervals = dictNeedRunMsg.get('run_intervals')

        self.intMintHour = dictNeedRunMsg.get('when_minute_in_hour')
        
        
        if(len(dictNeedRunMsg) > 1):
            #self.timingRun()
            self.runProcess(dictNeedRunMsg)
            #emailUtil = EmailUtil(dictNeedRunMsg, self.fileUtil)
        elif(len(dictNeedRunMsg) == 1):
            self.fileUtil.writerContent("配置文件参数值不全,未执行检测", 'runLog')
        else:
            self.fileUtil.writerContent("配置文件读取失败,未执行检测", 'runLog')
            
        emailUtil = EmailUtil(dictNeedRunMsg, self.fileUtil)

        if(self.fileUtil.boolWhetherShowLog & True):
            self.fileUtil.writerContent("============", 'runLog')
    
        timeingObject = Timer(int(intRunIntervals), self.timingRun)
        timeingObject.start()


    def runProcess(self, dictNeedRunMsg):

        #运行检测各个项目
        
        listKeys = dictNeedRunMsg.keys()
        for keyItem in listKeys:
            if(keyItem.find('tomcat') != -1):
                strTomcatPath = dictNeedRunMsg.get(keyItem)
                tomcatOperate = TomcatOperate(strTomcatPath, self.fileUtil.strMinTime, self.intMintHour,
                                              self.fileUtil)
                #print(strTomcatPath)
            if(keyItem.find('nginx') != -1):
                strNginxPath = dictNeedRunMsg.get(keyItem)
                nginxOperate = NginxOperate(strNginxPath, self.fileUtil.strMinTime, self.intMintHour,
                                            self.fileUtil)
                #print(strNginxPath)
            if(keyItem.find('redis') != -1):
                strRedisPath = dictNeedRunMsg.get(keyItem)
                redisOperate = RedisOperate(strRedisPath, self.fileUtil.strMinTime, self.intMintHour,
                                            self.fileUtil)
                #print(strRedisPath)
