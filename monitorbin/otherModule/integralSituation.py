#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg错过
# time  : 2018-04-25

from monitorbin.util.mysqlUtil import MySqlUtil
from monitorbin.util.sysTime import RunTime


class IntegralSit:

    # 获取积分使用详情
    # 此项为每天只检测一次

    strGetIntegralSituationSql = "sql/get-integralSituation.sql"

    def __init__(self, fileUtilObj, dataTempObj, dictNeedRunMsg, intNowHourTime, intHourCheckAll, allModuleRunAllObj):

        self.fileUtilObj = fileUtilObj
        self.dataTempObj = dataTempObj

        self.intNowHourTime = intNowHourTime
        self.intHourCheckAll = intHourCheckAll
        self.allModuleRunAllObj = allModuleRunAllObj

        self.runTimeObj = RunTime()
        self.mysqlUtilObj = MySqlUtil(self.fileUtilObj)

        if ((self.intNowHourTime == self.intHourCheckAll) or (self.intNowHourTime == ("0" + self.intHourCheckAll))):

            if (self.allModuleRunAllObj.intOverAllGetIntegralSit == 0):

                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("-->执行获取积分使用详情", 'runLog')

                dictMsgForMysql = self.mysqlUtilObj.getMsgForMysql(dictNeedRunMsg)
                if ((len(dictMsgForMysql) == 1) and ('err' in dictMsgForMysql)):
                    if (self.fileUtilObj.boolWhetherShowLog & True):
                        self.fileUtilObj.writerContent(("获取积分使用详情所需mysql信息不全,致检测任务中止"), 'runLog')
                else:

                    dateTodayBegin = self.runTimeObj.getTime("%Y-%m-%d")
                    self.intTodayBeginStamp = self.runTimeObj.getTimeStamp(str(dateTodayBegin), "%Y-%m-%d")

                    dateTodayEnd = self.runTimeObj.getDateTime()
                    self.intTodayEndStamp = self.runTimeObj.getTimeStamp(dateTodayEnd, "%Y-%m-%d %H:%M:%S")

                    self.doGetIntegralSit(dictMsgForMysql)

                self.allModuleRunAllObj.intOverAllGetIntegralSit = 1
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("今日获取积分使用详情已经标记为1", 'runLog')

            else:
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("-->获取积分使用详情今日已执行,今日将不再执行", 'runLog')
        else:
            if (self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("未到达时间,不执行获取积分使用详情", 'runLog')



    def doGetIntegralSit(self, dictMsgForMysql):

        # 查询并将数据存入模板

        strSqlContent = self.fileUtilObj.readFileContent(self.strGetIntegralSituationSql)
        strTotalSql = self.getToalSql(strSqlContent, self.intTodayBeginStamp, self.intTodayEndStamp)

        listResult = self.mysqlUtilObj.doSearchSql(strTotalSql, dictMsgForMysql)

        if (self.fileUtilObj.boolWhetherShowLog & True):
            self.fileUtilObj.writerContent(("获取积分使用详情sql: " + strTotalSql), 'runLog')
            self.fileUtilObj.writerContent(("获取到的结果为: " + str(listResult)), 'runLog')

        decTotalIntegNum = listResult[0].get('totalIntegralNum')
        if(decTotalIntegNum is None):
            decTotalIntegNum = 0

        intShopNum = listResult[0].get('totalShopNum')
        if(intShopNum is None):
            intShopNum = 0

        strResultContent = ("> - 查找到今日(截止至目前" + str(self.intNowHourTime) + "时)使用了积分的校区数总计 **" +
                            str(intShopNum) + "** 所,积分使用次数总计 **" + str(decTotalIntegNum) + "** 次")

        self.dataTempObj.dataAll += strResultContent + "\n\n"

        if (self.fileUtilObj.boolWhetherShowLog & True):
            self.fileUtilObj.writerContent(("生成数据如:" + strResultContent), 'runLog')


    def getToalSql(self, strSqlFileContent, intTodayBeginStamp, intTodayEndStamp):

        # 组合sql语句,从sql文件中读取到的sql语句中存在格式化字符%d
        # strSqlFileContent: 从sql文件中读取到的sql内容
        # intTodayBeginStamp: 前一天0点的时间戳
        # intTodayEndStamp: 运行当天-点的时间戳

        strNewSql = (strSqlFileContent % (intTodayBeginStamp, intTodayEndStamp))

        return strNewSql

