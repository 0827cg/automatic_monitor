# -*- coding: utf-8 -*-

import time
import datetime

# author: cg错过
# time: 2017-09-30

class RunTime:

    # 时间模块

    def getTime(self, strFormat):

        # 按照格式获取时间

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


    def getPastDataDay(self, intDayNum):

        # 根据天数，来获取过去距离今天intDayNum天的日期
        # intDayNum: int类型, 表示天数
        # 返回的是一个date对象类型的日期,格式是"%Y-%m-%d"

        strToday = datetime.date.today()

        # strToday的日期格式就是"%Y-%m-%d"
        strOtherday = strToday - datetime.timedelta(days = intDayNum)

        return strOtherday

    def getFutureDataDay(self, intDayNum):

        # 根据天数，来获取未来距离今天intDayNum天的日期
        # intDayNum: int类型, 表示天数
        # 返回的是一个date对象类型的日期,格式是"%Y-%m-%d"

        strToday = datetime.date.today()

        # strToday的日期格式就是"%Y-%m-%d"
        strOtherday = strToday + datetime.timedelta(days = intDayNum)

        return strOtherday

    
    def getTimeStamp(self, strDate, strFormatDate):
        
        # 根据日期，获取时间戳
        # strDate: 字符串类型的日期
        # strFormatDate: 与strDate先对应的日期格式，例如"%Y-%m-%d"
        # 返回一个int类型的时间戳
        
        timeArray = time.strptime(strDate, strFormatDate)
        timeStamp = time.mktime(timeArray)

        return int(timeStamp)

    def getTodayStamp(self):

        # 获取今天的时间戳
        # 返回的是一个int类型的时间戳,日期格式是"%Y-%m-%d"

        strToday = datetime.date.today()
        timeArray = time.strptime(str(strToday), "%Y-%m-%d")
        timeStamp = time.mktime(timeArray)

        return int(timeStamp)


    def doCutHorizontalLine(self, strData):

        # 用来将日期中存在的'-'删除,返回一个没有'-'的日期字符串
        # strData: 存在’-‘的日期字符串
        
        listNewStrData = []
        listStrData = list(strData)
        for listStrDataItem in listStrData:
            if(listStrDataItem == '-'):
                pass
            else:
                listNewStrData.append(listStrDataItem)
        return ''.join(listNewStrData)
            

    
