#!/usr/bin/python3
#coding=utf-8

import time

#author: cg错过
#time: 2017-09-30

class RunTime:

    #时间模块

    def getTime(self, strFormat):

        #按照格式获取时间

        nowTime = time.localtime()
        strFormatTime = time.strftime(strFormat, nowTime)
        return strFormatTime

    def getDateTime(self):
        return self.getTime("%Y-%m-%d %H:%M:%S")

    def getNumSecondTime(self):
        return self.getTime("%Y%m%d%H%M%S")

    def getNumHourTime(self):
        return self.getTime("%Y%m%d%H")

    def getNumDayTime(self):
        return self.getTime("%Y%m%d")

    def getMinTime(self):
        return self.getTime("%M")

    def getHourTime(self):
        return self.getTime("%H")

    def getHourMinTime(self):
        return self.getTime("%H%M")
