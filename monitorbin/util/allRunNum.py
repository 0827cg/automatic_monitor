#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg错过
# time  : 2017-12-12

class AllModuleRunAll:

    # 为实现在规定之间内只执行一次，
    # 例如在小时数为9的时候，这个小时内只执行一次检测
    # 这个类只是提供一个判断条件
    # 当然也可以利用此条件来执行几次，就看后面调用时的代码怎么写了

    # 2017-12-14添加intOverAllCheckPicArrivals,intOverAllCheckPm2
    # 2018-04-25添加intOverAllCountNum, intOverAllGetIntegralSit

    intOverAllCheckTomcatNum = 0
    intOverAllCheckNginxNum = 0
    intOverAllCheckRedisNum = 0
    intOverAllCheckLetterNum = 0
    intOverAllCheckDiskNum = 0
    intOverAllCheckPicArrivals = 0
    intOverAllCheckPm2 = 0
    intOverAllCountNum = 0
    intOverAllGetIntegralSit = 0

    '''

    def setTomcatValue(self, value):

        self.intOverAllCheckTomcatNum = value
    
    def setNginxValue(self, value):

        self.intOverAllCheckNginxNum = value
        
    def setRedisValue(self, value):

        self.intOverAllCheckRedisNum = value

    def setLetterValue(self, value):

        self.intOverAllCheckLetterNum = value

    def setDiskValue(self, value):

        self.intOverAllCheckDiskNum = value

    '''

    def initAllNum(self):

        # 重置所有项目一天执行状态为0，即表示未执行,新一天将继续执行

        intIndex = 0

        if((self.intOverAllCheckTomcatNum == 1) | (self.intOverAllCheckNginxNum == 1) |
           (self.intOverAllCheckRedisNum == 1) | (self.intOverAllCheckLetterNum == 1) |
           (self.intOverAllCheckDiskNum == 1) | (self.intOverAllCheckPicArrivals ==1) |
           (self.intOverAllCheckPm2 == 1) | (self.intOverAllCountNum == 1) | (self.intOverAllGetIntegralSit == 1)):

            self.intOverAllCheckTomcatNum = 0
            self.intOverAllCheckNginxNum = 0
            self.intOverAllCheckRedisNum = 0
            self.intOverAllCheckLetterNum = 0
            self.intOverAllCheckDiskNum = 0
            self.intOverAllCheckPicArrivals = 0
            self.intOverAllCheckPm2 = 0
            self.intOverAllCountNum = 0
            self.intOverAllGetIntegralSit = 0

            intIndex = 1

        return intIndex
