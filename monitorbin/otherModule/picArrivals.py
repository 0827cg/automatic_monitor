#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg错过
# time: 2017-12-14

from monitorbin.util.mysqlConnect import DoMysql
from monitorbin.util.sysTime import RunTime
from monitorbin.otherModule.picArrivalCompare import PicArrivalCompare

class PicArrivals:

    # 检测图片到达率
    # 根据其配置,一天只检测一次
    # 获取前一天总的图片到达率

    # 添加获取当前的图片到达率

    def __init__(self, fileUtilObj, dictNeedRunMsg, dataTemplateObj, intHourTime, intHourCheckAll,
                 allModuleRunAllObj):

        self.fileUtilObj = fileUtilObj
        self.dataTemplateObj = dataTemplateObj
        self.intHourTime = intHourTime
        self.intHourCheckAll = intHourCheckAll
        self.allModuleRunAllObj = allModuleRunAllObj

        if((self.intHourTime == self.intHourCheckAll) or (self.intHourTime == ("0" + self.intHourCheckAll))):
            
            if(self.allModuleRunAllObj.intOverAllCheckPicArrivals == 0):

                dictMsgForMysql = self.getMsgForMysql(dictNeedRunMsg)
                dictMsgForCheckPic = self.getMsgForCheckPic(dictNeedRunMsg)
                
                self.checkTogToday(dictMsgForMysql, dictMsgForCheckPic)
                
                self.allModuleRunAllObj.intOverAllCheckPicArrivals = 1
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("今日检测图片到达率次数已标记为" +
                                                   str(self.allModuleRunAllObj.intOverAllCheckPicArrivals)), 'runLog')
            else:   
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("今日" + str(self.intHourCheckAll) +
                                                "内已检测图片到达率,今日将不再全面检测\n" +
                                                 "将进行错误监控任务"), 'runLog')



    def checkTog(self, dictMsgForMysql, dictMsgForCheckPic):

        # 检测

        self.runTime = RunTime()

        self.dateYesterday = self.runTime.getPastDataDay(1)
        self.intYesterdayStamp = self.runTime.getTimeStamp(str(self.dateYesterday), "%Y-%m-%d")
        self.intTodayStamp = self.runTime.getTodayStamp()

        if(self.fileUtilObj.boolWhetherShowLog & True):
            self.fileUtilObj.writerContent(("-->检测" + str(self.dateYesterday) + "图片到达率"), 'runLog')
            
        if(((len(dictMsgForMysql) == 1) and ('err' in dictMsgForMysql)) or
           ((len(dictMsgForCheckPic) == 1) and ('err' in dictMsgForCheckPic))):
            if(self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("检测图片到达率所需配置信息不全,致检测任务中止", 'runLog')
        else:
            
            self.strSearchSql = dictMsgForCheckPic.get('sql_path')
            self.intAccuracy = dictMsgForCheckPic.get('number_accuracy')
            intArrivalsStandart = int(dictMsgForCheckPic.get('arrivals_standard'))

            intMark = self.fileUtilObj.checkFileExists(self.strSearchSql)
            if(intMark == 1):
                strSqlContent = self.fileUtilObj.readFileContent(self.strSearchSql)
                strTotalSearchSql = self.getToalSql(strSqlContent, self.intYesterdayStamp, self.intTodayStamp)
                listResultFirst = self.doSearchSql(strTotalSearchSql, dictMsgForMysql)
                listResult = self.rmoveDecimal(listResultFirst)
                listMsgForLog = self.getSomeForLog(listResult)

                picArrivalCompare = PicArrivalCompare(self.fileUtilObj, self.dataTemplateObj)
                
                listNewResultSome = self.getSomeMsg(listResult, intArrivalsStandart)

                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("查找到的机构信息如下:", 'runLog')
                
                for listMsgForLogItem in listMsgForLog:   
                    if(self.fileUtilObj.boolWhetherShowLog & True):
                        self.fileUtilObj.writerContent((str(listMsgForLogItem)), 'runLog')

                dictValue = self.getAverageValue(listResult)

                self.dataTemplateObj.dataAll += (" > - 查找到 **" + str(dictValue.get('totalNum')) +
                                                 "** 家机构有使用签到,并于" + str(self.dateYesterday) +
                                                 "一天内总共的图片平均到达率为 **" +
                                                 str(dictValue.get('averageValue')) + "%** ,其中到达率低于" +
                                                 str(intArrivalsStandart) + "%的有 **" +
                                                 str(len(listNewResultSome)) + "** 家机构\n")
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("查找到" + str(dictValue.get('totalNum')) +
                                                 "家机构有使用签到,并于" + str(self.dateYesterday) +
                                                 "一天内总共的图片平均到达率为" +
                                                 str(dictValue.get('averageValue')) + "%,其中到达率低于" +
                                                    str(intArrivalsStandart) + "%的有" +
                                                 str(len(listNewResultSome)) + "家机构"), 'runLog')

                picArrivalCompare.compareData(listResult)
                picArrivalCompare.writerListTotalToFile(listResult)

                
            else:
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("未发现" + self.strSearchSql + "文件,将停止检测"), 'runLog')

    def checkTogToday(self, dictMsgForMysql, dictMsgForCheckPic):

        # 检测

        # 检测当天(从零点截止至当前运行此方法的时刻)的图片到达率
        # 添加此方法的原因是需求变了，即获取当天的数据。--添加于2018-03-14


        self.runTime = RunTime()

        # self.dateYesterday = self.runTime.getPastDataDay(1)
        # self.intYesterdayStamp = self.runTime.getTimeStamp(str(self.dateYesterday), "%Y-%m-%d")
        # self.intTodayStamp = self.runTime.getTodayStamp()

        dateTodayBegin = self.runTime.getTime("%Y-%m-%d")
        intTodayBeginStamp = self.runTime.getTimeStamp(str(dateTodayBegin), "%Y-%m-%d")

        dateTodayEnd = self.runTime.getDateTime()
        intTodayEndStamp = self.runTime.getTimeStamp(dateTodayEnd, "%Y-%m-%d %H:%M:%S")

        if (self.fileUtilObj.boolWhetherShowLog & True):
            self.fileUtilObj.writerContent(("-->检测" + str(dateTodayBegin) + "图片到达率"), 'runLog')

        if (((len(dictMsgForMysql) == 1) and ('err' in dictMsgForMysql)) or
                ((len(dictMsgForCheckPic) == 1) and ('err' in dictMsgForCheckPic))):
            if (self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("检测图片到达率所需配置信息不全,致检测任务中止", 'runLog')
        else:

            self.strSearchSql = dictMsgForCheckPic.get('sql_path')
            self.intAccuracy = dictMsgForCheckPic.get('number_accuracy')
            intArrivalsStandart = int(dictMsgForCheckPic.get('arrivals_standard'))

            intMark = self.fileUtilObj.checkFileExists(self.strSearchSql)
            if (intMark == 1):
                strSqlContent = self.fileUtilObj.readFileContent(self.strSearchSql)
                strTotalSearchSql = self.getToalSql(strSqlContent, intTodayBeginStamp, intTodayEndStamp)
                listResultFirst = self.doSearchSql(strTotalSearchSql, dictMsgForMysql)
                listResult = self.rmoveDecimal(listResultFirst)
                listMsgForLog = self.getSomeForLog(listResult)

                picArrivalCompare = PicArrivalCompare(self.fileUtilObj, self.dataTemplateObj)

                listNewResultSome = self.getSomeMsg(listResult, intArrivalsStandart)

                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("查找到的机构信息如下:", 'runLog')

                for listMsgForLogItem in listMsgForLog:
                    if (self.fileUtilObj.boolWhetherShowLog & True):
                        self.fileUtilObj.writerContent((str(listMsgForLogItem)), 'runLog')

                dictValue = self.getAverageValue(listResult)

                self.dataTemplateObj.dataAll += (" > - 查找到 **" + str(dictValue.get('totalNum')) +
                                                 "** 家机构有使用签到,并于" + str(dateTodayBegin) +
                                                 "一天内总共的图片平均到达率为 **" +
                                                 str(dictValue.get('averageValue')) + "%** ,其中到达率低于" +
                                                 str(intArrivalsStandart) + "%的有 **" +
                                                 str(len(listNewResultSome)) + "** 家机构\n")
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("查找到" + str(dictValue.get('totalNum')) +
                                                    "家机构有使用签到,并于" + str(dateTodayBegin) +
                                                    "一天内总共的图片平均到达率为" +
                                                    str(dictValue.get('averageValue')) + "%,其中到达率低于" +
                                                    str(intArrivalsStandart) + "%的有" +
                                                    str(len(listNewResultSome)) + "家机构"), 'runLog')

                picArrivalCompare.compareData(listResult)
                picArrivalCompare.writerListTotalToFile(listResult)


            else:
                if (self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent(("未发现" + self.strSearchSql + "文件,将停止检测"), 'runLog')

    def getAverageValue(self, listResult):

        # listResult: 所有数据,包括达到100的
        # 统计平均值
        # dict里存放的字段有
        # totalNum: 所有机构个数
        # averageValue: 图片到达率平均值

        dictValue = {}
        intTotalNum = len(listResult)
        floatTotalValue = 0.0

        if(intTotalNum != 0):

            for listResultItem in listResult:
                floatValue = float(listResultItem.get('rate'))
                floatTotalValue += floatValue
                
            floatAverageValue = (floatTotalValue / intTotalNum)
        else:
            floatAverageValue = 0.00
        
        dictValue['totalNum'] = intTotalNum
        dictValue['averageValue'] = round(floatAverageValue, int(self.intAccuracy))

        return dictValue
        

    
    def getToalSql(self, strSqlFileContent, intTodayBeginStamp, intTodayEndStamp):

        # 组合sql语句,从sql文件中读取到的sql语句中存在格式化字符%d
        # strSqlFileContent: 从sql文件中读取到的sql内容
        # intTodayBeginStamp: 前一天0点的时间戳
        # intTodayEndStamp: 运行当天-点的时间戳

        strNewSql = (strSqlFileContent %(intTodayBeginStamp, intTodayEndStamp))

        return strNewSql


    def doSearchSql(self, strSearchSql, dictMsgForMysql):

        # 执行sql语句,这里用来做查找
        # strSql: 要执行的sql语句

        listResult = []
        doMySql = DoMysql(dictMsgForMysql)
        connectionObj = doMySql.connectionMySQL()
        
        if(connectionObj is None):
            if(self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("数据库查询图片到达率连接失败", 'runLog')
        else:
            if(self.fileUtilObj.boolWhetherShowLog & True):
                self.fileUtilObj.writerContent("数据库查询图片到达率已连接", 'runLog')

            try:
                with connectionObj.cursor() as cursor:

                    cursor.execute(strSearchSql)
                    listResult = cursor.fetchall()
                    
                if(len(listResult) == 0 ):
                    if(self.fileUtilObj.boolWhetherShowLog & True):
                        self.fileUtilObj.writerContent("未查找到数据", 'runLog')

            except:
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("查询时出错", 'runLog')

            finally:
                connectionObj.close()
                if(self.fileUtilObj.boolWhetherShowLog & True):
                    self.fileUtilObj.writerContent("数据库查询图片连接已关闭", 'runLog')

        return listResult

    def rmoveDecimal(self, listResult):

        # 去除decimal

        listNewResult = []
        for listResultItem in listResult:
            dictResultItem = {}
            dictResultItem['org_name'] = listResultItem.get('org_name')
            dictResultItem['shop_name'] = listResultItem.get('shop_name')
            dictResultItem['org_id'] = listResultItem.get('org_id')
            dictResultItem['shop_id'] = listResultItem.get('shop_id')
            dictResultItem['rate'] = float(listResultItem.get('rate'))
            listNewResult.append(dictResultItem)
        return listNewResult



    def getSomeMsg(self, listResult, intRate):

        # listResult:搜索到的全部数据
        # intRate: 参数，这里例如为80
        # 提起出到达率为达到80的机构

        listNewResult = []

        for listResultItem in listResult:
            if(float(listResultItem.get('rate')) <= float(intRate)):
                listNewResult.append(listResultItem)

        return listNewResult


    def getSomeForLog(self, listResult):

        # 获取机构的部分数据，为显示在log文件上
        # listResult: 查找到的全部数据

        listTitle = ["机构名", "校区名", "机构id", "校区id", "图片到达率"]
        listSomeForLog = []
        listSomeForLog.append(listTitle)
        for listResultItem in listResult:
            listSomeForLogItem = []
            
            strOrgName = listResultItem.get('org_name')
            strShopName = listResultItem.get('shop_name')
            strOrgId = listResultItem.get('org_id')
            strShopId = listResultItem.get('shop_id')
            strRate = listResultItem.get('rate')
            
            listSomeForLogItem.append(strOrgName)
            listSomeForLogItem.append(strShopName)
            listSomeForLogItem.append(strOrgId)
            listSomeForLogItem.append(strShopId)
            listSomeForLogItem.append(strRate)

            listSomeForLog.append(listSomeForLogItem)
            
        return listSomeForLog
            
        
        


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
            if((keyItem == 'host') | (keyItem == 'port') |
               (keyItem == 'user') | (keyItem == 'passwd') | (keyItem == 'database')):
                if(dictNeedRunMsg.get(keyItem) != ''):
                    
                    dictMsgForMysql[keyItem] = dictNeedRunMsg.get(keyItem)
                else:
                    dictMsgForMysql.clear()
                    dictMsgForMysql['err'] = "Msg Incomplete"
                    break
                
        return dictMsgForMysql


    def getMsgForCheckPic(self, dictNeedRunMsg):

        # 获取检测图片到达率所需的数据,并判断数据是否完全
        # 返回一个dict类型的数据
        # sql_path: 存放sql语句的文件路径及文件名
        # number_accuracy: 保留的小数的个数,精度范围
        # arrivals_standard: 到达率的一个标准

        dictMsgForCheckPic = {}
        for keyItem in dictNeedRunMsg:
            if((keyItem == 'sql_path') | (keyItem == 'number_accuracy') |
               (keyItem == 'arrivals_standard')):
                if(dictNeedRunMsg.get(keyItem) != ''):
                    dictMsgForCheckPic[keyItem] = dictNeedRunMsg.get(keyItem)
                else:
                    dictMsgForCheckPic.clear()
                    dictMsgForCheckPic['err'] = "Msg Incomplete"
                    break
        return dictMsgForCheckPic





