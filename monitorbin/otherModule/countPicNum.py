#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg错过
# time  : 2018-04-24

from monitorbin.util.mysqlConnect import DoMysql
from monitorbin.util.sysTime import RunTime

class CountPicNum:

    # 统计'动态','食谱'这两项当天上传的图片数量
    # 此项为每天只检测一次
    # 打算在这里将存放sql语句的文件写死

    strGetFoodPicNumSql = "sql/get-foodPicNum.sql"
    strGetDynamicPicNumSql = "sql/get-dynamicPicNum.sql"


    def __init__(self, fileUtilObj, dataTempObj, dictNeedRunMsg, intNowHourTime, intHourCheckAll, allModuleRunAllObj):

        self.fileUtilObj = fileUtilObj
        self.dataTempObj = dataTempObj
        self.runTimeObj = RunTime()

        self.intNowHourTime = intNowHourTime
        self.intHourCheckAll = intHourCheckAll

        self.allModuleRunAllObj = allModuleRunAllObj

        if ((self.intNowHourTime == self.intHourCheckAll) or (self.intNowHourTime == ("0" + self.intHourCheckAll))):

            if(self.allModuleRunAllObj.intOverAllCountNum == 0):

                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("-->执行统计图片数量", 'runLog')

                dictMsgForMysql = self.getMsgForMysql(dictNeedRunMsg)

                if ((len(dictMsgForMysql) == 1) and ('err' in dictMsgForMysql)):
                    if (self.fileUtilObj.boolWhetherShowLog & True):
                        self.fileUtilObj.writerContent(("统计'动态','食谱'图片数量所需配置信息不全,致检测任务中止"), 'runLog')
                else:

                    dateTodayBegin = self.runTimeObj.getTime("%Y-%m-%d")
                    self.intTodayBeginStamp = self.runTimeObj.getTimeStamp(str(dateTodayBegin), "%Y-%m-%d")

                    dateTodayEnd = self.runTimeObj.getDateTime()
                    self.intTodayEndStamp = self.runTimeObj.getTimeStamp(dateTodayEnd, "%Y-%m-%d %H:%M:%S")

                    self.doCount(dictMsgForMysql, dictNeedRunMsg)

                self.allModuleRunAllObj.intOverAllCountNum = 1
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("今日统计图片数量操作已经标记为1", 'runLog')

            else:
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("-->统计图片数量今日已执行,今日将不再执行", 'runLog')

        else:
            if (self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("未到达时间,不执行统计图片数量", 'runLog')


    def doCount(self, dictMsgForMysql, dictNeedRunMsg):

        # 总执行

        if 'whether_count_food' in dictNeedRunMsg:
            if dictNeedRunMsg.get('whether_count_food') == 'yes':
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("开始统计食谱的图片数量", 'runLog')
                listResult = self.getCountFoodPicNum(dictMsgForMysql)
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("获取到的结果为:" + str(listResult)), 'runLog')
                floatFoodPicNum = listResult[0].get('foodPicNum')

                if(floatFoodPicNum is None):
                    floatFoodPicNum = 0

                strSendData = ("> - 查找到今日(截止至目前" + str(self.intHourCheckAll) +
                                             "时)食谱中上传的图片有 **" + str(floatFoodPicNum) + "** 张")
                self.dataTempObj.dataAll += strSendData + "\n\n"

                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("生成数据如: " + strSendData, 'runLog')

            else:
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("不统计食谱的图片数量", 'runLog')

        if 'whether_count_dynamic' in dictNeedRunMsg:
            if dictNeedRunMsg.get('whether_count_dynamic') == 'yes':
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("开始统计动态的图片数量", 'runLog')
                listResult = self.getCountDynamicPicNum(dictMsgForMysql)
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("获取到的结果为:" + str(listResult)), 'runLog')
                floatDynamicPicNum = listResult[0].get('dynamicPicNum')

                if(floatDynamicPicNum is None):
                    floatDynamicPicNum = 0

                strSendData = ("> - 查找到今日(截止至目前" + str(self.intHourCheckAll) +
                                             "时)动态中上传的图片有 **" + str(floatDynamicPicNum) + "** 张")
                self.dataTempObj.dataAll += strSendData + "\n\n"

                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("生成数据如: " + strSendData, 'runLog')


            else:
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("不统计动态的图片数量", 'runLog')


    def getCountFoodPicNum(self, dictMsgForMysql):

        # 查询食谱图片数量

        strCountFoodPicSql = self.fileUtilObj.readFileContent(self.strGetFoodPicNumSql)
        strTotalSql = self.getToalSql(strCountFoodPicSql, self.intTodayBeginStamp, self.intTodayEndStamp)

        if (self.fileUtilObj.boolWhetherShowLog & True):
            self.fileUtilObj.writerContent(("查询食谱图片数量sql: " + strTotalSql), 'runLog')

        listResult = self.doSearchSql(strTotalSql, dictMsgForMysql)

        # print("listResult: ")
        # print(str(listResult))
        return listResult



    def getCountDynamicPicNum(self, dictMsgForMysql):

        # 查询动态图片数量

        strCountDynamicPicSql = self.fileUtilObj.readFileContent(self.strGetDynamicPicNumSql)
        strTotalSql = self.getToalSql(strCountDynamicPicSql, self.intTodayBeginStamp, self.intTodayEndStamp)

        if (self.fileUtilObj.boolWhetherShowLog & True):
            self.fileUtilObj.writerContent(("查询动态图片数量sql: " + strTotalSql), 'runLog')

        listResult = self.doSearchSql(strTotalSql, dictMsgForMysql)
        return listResult


    def doSearchSql(self, strSearchSql, dictMsgForMysql):

        # 执行sql语句,这里用来做查找
        # strSql: 要执行的sql语句

        listResult = []
        doMySql = DoMysql(dictMsgForMysql)
        connectionObj = doMySql.connectionMySQL()

        if (connectionObj is None):
            if (self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("数据库查询连接失败", 'runLog')
        else:
            if (self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("数据库查询已连接", 'runLog')

            try:
                with connectionObj.cursor() as cursor:

                    cursor.execute(strSearchSql)
                    listResult = cursor.fetchall()

                if (len(listResult) == 0):
                    if (self.fileUtilObj.boolWhetherShowLog & True):
                        self.fileUtilObj.writerContent("未查找到数据", 'runLog')

            except:
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("查询时出错", 'runLog')

            finally:
                connectionObj.close()
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("数据库查询连接已关闭", 'runLog')

        return listResult


    def getToalSql(self, strSqlFileContent, intTodayBeginStamp, intTodayEndStamp):

        # 组合sql语句,从sql文件中读取到的sql语句中存在格式化字符%d
        # strSqlFileContent: 从sql文件中读取到的sql内容
        # intTodayBeginStamp: 前一天0点的时间戳
        # intTodayEndStamp: 运行当天-点的时间戳

        strNewSql = (strSqlFileContent % (intTodayBeginStamp, intTodayEndStamp))

        return strNewSql


    def getMsgForMysql(self, dictNeedRunMsg):

        # 获取连接mysql数据库所需要的数据，并判断是否完全
        # 返回一个dict类型的数据
        # 存放的字段
        # host
        # port
        # user
        # passwd
        # database

        dictMsgForMysql = {}

        for keyItem in dictNeedRunMsg:
            if ((keyItem == 'host') | (keyItem == 'port') |
                    (keyItem == 'user') | (keyItem == 'passwd') | (keyItem == 'database')):
                if (dictNeedRunMsg.get(keyItem) != ''):

                    dictMsgForMysql[keyItem] = dictNeedRunMsg.get(keyItem)
                else:
                    dictMsgForMysql.clear()
                    dictMsgForMysql['err'] = "Msg Incomplete"
                    break

        return dictMsgForMysql


