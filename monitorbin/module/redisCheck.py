#!/usr/bin/python3
#coding=utf-8

import os
from monitorbin.util.process import ProcessCL

#author: cg错过
#time: 2017-09-30

class RedisOperate:

    #redis检测模块
    
    def __init__(self, strRedisPath, intHourTime, intHourCheckAll, fileUtilObj):

        #strRedisPath: redis的安装文件目录
        #intHourTime: 当前运行脚本的小时数
        #intHourCheckAll: 配置文件中设置的时间(小时数)
        #fileUtilObj: FileUtil的对象(脚本从运行到结束都只有这一个FileUtil对象)

        #2017-12-08将分钟数改为小时，即每天大检测只执行一次

        self.fileUtil = fileUtilObj
        self.intHourTime = intHourTime
        self.intHourCheckAll = intHourCheckAll
        self.strRedisPath = strRedisPath
        
        if(self.fileUtil.boolWhetherShowLog & True):
            self.fileUtil.writerContent("-->准备检测redis", 'runLog')
            self.fileUtil.writerContent("检测redis路径...", 'runLog')
            
        intCheckResult = self.fileUtil.checkFileExists(self.strRedisPath)
        if(intCheckResult == 1):
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("redis路径存在,将执行检测redis", 'runLog')
            self.checkRedis()
        else:
            self.fileUtil.writerContent("配置的redis路径不存在", 'runLog')
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("redis检测模块将退出", 'runLog')

    def checkRedis(self):

        #每个小时检测一遍，不做操作
        #其他时候，当检测到未运行时，脚本尝试自启一次

        strRedisStatus = self.getRedisStatus()

        if(self.intHourTime == self.intHourCheckAll):
            self.checkRedisStatus(strRedisStatus)
        else:
            intMark = self.checkRedisStatus(strRedisStatus, 'Second')
            if(intMark == -1):
                self.tryStartRedis(self.strRedisPath)


    def getRedisStatus(self):

        #获取进程中的redis

        redisStatusCL = "ps -ef | grep redis"
        processCL = ProcessCL()
        dictResult = processCL.getResultAndProcess(redisStatusCL)
        strRedisStatus = dictResult.get('stdout')
        return strRedisStatus


    def checkRedisStatus(self, strRedisStatus, strFileMark='Hour'):

        #判断redis是否运行

        intMark = -1
        strRedis = "redis-server"

        if(strRedisStatus.find(strRedis) != -1):
            #print("redis在运行")
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("redis在运行")
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent("redis在运行", 'runLog')
            intMark = 1
        else:
            if(strFileMark=='Hour'):
                self.fileUtil.writerContent("redis未运行")
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent("redis未运行", 'runLog')
            else:
                self.fileUtil.writerContent("redis未运行", 'Second')
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent("redis未运行", 'runLog')
            #print("redis未运行")
        return intMark


    def tryStartRedis(self, strRedisPath):

        #脚本启动redis

        intMark = -1
        #print("脚本尝试将其启动....")
        #print(strRedisPath)
        self.fileUtil.writerContent("脚本尝试将其启动...", 'Second')
        if(self.fileUtil.boolWhetherShowLog & True):
            self.fileUtil.writerContent("脚本尝试将其启动...", 'runLog')
        strStartRedisCL = strRedisPath + "/src/./redis-server"
        processCL = ProcessCL()
        dictResult = processCL.getContinueResultAndProcess(strStartRedisCL)
        strOut = dictResult.get('stdout')
        strErr = dictResult.get('stderr')
        if(strOut.find('redis.io') != -1):
            self.fileUtil.writerContent("redis已被脚本启动", 'Second')
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("redis已被脚本启动", 'runLog')
            #print("redis已被脚本启动成功")
            intMark = 1
        else:
            #print("脚本启动redis未成功，请手动启动")
            self.fileUtil.writerContent("脚本启动redis未成功，请手动启动", 'Second')
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("脚本启动redis未成功，请手动启动", 'runLog')
            self.fileUtil.writerErr(("redis: " + strErr), 'Second')
            #print(strErr)
        return intMark
        
        
