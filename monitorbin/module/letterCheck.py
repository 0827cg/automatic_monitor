# -*- coding: utf-8 -*-

#author: cg错过
#time: 2017-12-08

from monitorbin.util.mysqlConnect import DoMysql
from monitorbin.util.sysTime import RunTime
import time


class CheckLetter:

    #检测数据库表中某个字段

    def __init__(self, fileUtilObj, dataTemplateObj, dictNeedRunMsg,  intHourTime, intHourCheckAll,
                 allModuleRunAllObj):

        self.fileUtil = fileUtilObj
        self.dataTemplate = dataTemplateObj
        self.runTime = RunTime()
        self.allModuleRunAllObj = allModuleRunAllObj
        
        self.intHourTime = intHourTime
        self.intHourCheckAll = intHourCheckAll

        intPastDaysNum = int(dictNeedRunMsg.get('past_days_num'))
        strPastDay = str(self.runTime.getPastDataDay(intPastDaysNum))
        self.intPastTimeStamp = self.runTime.getTimeStamp(strPastDay, "%Y-%m-%d")

        self.dataYesterday = self.runTime.getPastDataDay(1)
        
        if(self.fileUtil.boolWhetherShowLog & True):
            self.fileUtil.writerContent(("-->执行检测数据库字段任务"), 'runLog')

        dictMsgForCheckLetter = self.getMsgForCheckLetter(dictNeedRunMsg)
        dictMsgForMysql = self.getMsgForMysql(dictNeedRunMsg)

        if(((len(dictMsgForCheckLetter) == 1) and ('err' in dictMsgForCheckLetter)) or
           ((len(dictMsgForMysql) == 1) and ('err' in dictMsgForMysql))):
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("检测数据库字段所需配置不全, 致检测任务中止运行", 'runLog')
        else:

            self.strTable = dictMsgForCheckLetter.get('table_name')
            self.strField = dictMsgForCheckLetter.get('field_name')
            self.strFieldCompare1 = dictMsgForCheckLetter.get('fieldcompare_name1')
            self.strFieldCompare2 = dictMsgForCheckLetter.get('fieldcompare_name2')
            self.strFieldCompare3 = dictMsgForCheckLetter.get('fieldcompare_name3')
            self.strFieldCompare4 = dictMsgForCheckLetter.get('fieldcompare_name4')
            self.strFieldCompareValue = dictMsgForCheckLetter.get('fieldcompare_namevalue')
            self.intFirst = int(dictMsgForCheckLetter.get('first_field_value'))
            self.intNext = int(dictMsgForCheckLetter.get('next_field_value'))
            self.intSleepTime = int(dictMsgForCheckLetter.get('sleeptime'))

            self.checkRun(dictMsgForMysql)


    def checkRun(self, dictMsgForMysql):

        #执行检测
        #这个检测数据库字段并未分时间段
        #其他的项目检测就分了大任务和小任务检测，即按时和按分检测
        #这个就没有，因为数据库中的字段都是时刻在变化

        #2017-12-12添加大小任务，大任务统计前一天已推送和未推送的数据
        
        if((self.intHourTime == self.intHourCheckAll) or (self.intHourTime == ("0" + self.intHourCheckAll))):

            if(self.allModuleRunAllObj.intOverAllCheckLetterNum == 0):

                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("执行检测" + str(self.dataYesterday) + "的推送情况"), 'runLog')

                

                listNoSendMsg = self.getNoSendMsgYesterday(dictMsgForMysql)
                intNoSendNum = len(listNoSendMsg)
                
                intAlreadySendNum = self.getAlreadySendNumYesterday(dictMsgForMysql)

                self.dataTemplate.dataAll += ("> - " + str(self.dataYesterday) + "已推送" +
                                              str(intAlreadySendNum) + "条,未推送总数为" + str(intNoSendNum) +
                                              "条\n")

                if(intNoSendNum != 0):
                    self.dataTemplate.dataAll += ("> \t\t 其未推送的信息如下:\n")
                    if(self.fileUtil.boolWhetherShowLog & True):
                        self.fileUtil.writerContent("未推送的信息如下:", 'runLog')
                    for listNoSendMsgItem in listNoSendMsg:
                        if(self.fileUtil.boolWhetherShowLog & True):
                            self.fileUtil.writerContent((str(listNoSendMsgItem) + "\n"), 'runLog')
                        self.dataTemplate.dataAll += ("> \t\t " + str(listNoSendMsgItem) + "\n")

                self.allModuleRunAllObj.intOverAllCheckLetterNum = 1
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("今日检测数据库字段次数已标记为" +
                                                str(self.allModuleRunAllObj.intOverAllCheckLetterNum)), 'runLog')
                
            else:
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("今日" + str(self.intHourCheckAll) +
                                                "内已检测数据库字段,今日将不再全面检测\n" +
                                                 "将进行错误监控任务"), 'runLog')

                #配置文件中的when_hour_checkall时内进行错误监控,和下面else内一样
                self.checkTog(dictMsgForMysql)
                        
        else:
            self.checkTog(dictMsgForMysql)


    def checkTog(self, dictMsgForMysql):

        doMySql = DoMysql(dictMsgForMysql)
        objConnection = doMySql.connectionMySQL()

        listResult = self.findTheField(objConnection)
        listNewResult = self.findWhetherTheField(listResult, self.intSleepTime, dictMsgForMysql)

        if(self.fileUtil.boolWhetherShowLog & True):
            self.fileUtil.writerContent("检测已完成", 'runLog')


    def findTheField(self, objConnection):

        #查找设定表中的设定字段的值
        #若发现该字段的值为intFirst值，则进行时间性的间隔判断
        #将查找到的shopid和studentId值存放到一个字典中
        #objConnection: 数据库的一条连接
        #strTable: 表名
        #strField: 字段名
        #intFirst: 字段名的值(第一次的值，该值在规定时间秒后会发生更改)
        #intNext: 字段名更改后的值
        #获取之后将其返回，类型为list集合

        listResult = []

        if objConnection is None:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("数据库连接失败", 'runLog')
        else:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("数据库连接成功", 'runLog')
                self.fileUtil.writerContent((("查找" + self.strField + "值为%d" + "的数据") %(self.intFirst)),
                                            'runLog')

            try:
                with objConnection.cursor() as cursor:
                    strSearchSql = ("SELECT " + self.strFieldCompare1 + " , " + self.strFieldCompare2 +
                                    " , " + self.strFieldCompare3 + 
                                    " FROM " + self.strTable + " WHERE " + self.strField + "= %d AND " +
                                    self.strFieldCompareValue + " != " + "'" + "'" + " AND " +
                                    self.strFieldCompareValue + " IS NOT NULL" + " AND " +
                                    self.strFieldCompareValue + " != " + "'" + "null" + "'" + " AND " +
                                    self.strFieldCompare4 + " >= %d")
                    
                    cursor.execute(strSearchSql %(self.intFirst, self.intPastTimeStamp))
                    listResult = cursor.fetchall()

                    cursor.close()

                    if listResult is None:
                        if(self.fileUtil.boolWhetherShowLog & True):
                            self.fileUtil.writerContent((("未查找到" + self.strField + "值为%d" +
                                                         "的数据") %(self.intFirst)), 'runLog')
                    else:
                        if(self.fileUtil.boolWhetherShowLog & True):
                            self.fileUtil.writerContent(("已查找到%d条数据" %(len(listResult))), 'runLog')
                        for listResultItem in listResult:
                            self.fileUtil.writerContent(str(listResultItem), 'runLog')
                        #findWhetherTheField(objConnection, strTable, strField, intFirst, intNext, listResult)
                        
            finally:
                if objConnection._closed:
                    if(self.fileUtil.boolWhetherShowLog & True):
                        self.fileUtil.writerContent("第一次查询连接意外关闭", 'runLog')
                else:
                    objConnection.close()
                    if(self.fileUtil.boolWhetherShowLog & True):
                        self.fileUtil.writerContent("第一次查询连接已正常关闭", 'runLog')
                    
        return listResult


    def findWhetherTheField(self, listResult, intTime, dictMsgForMysql):

        #这个方法里，需要与数据库建立一条新的连接
        #strTable: 表名
        #strField: 字段名
        #intNext: 字段名更改后的值
        #listResult: 字段名的值为第一次更改前的集合，集合中包括shopid,studentId
        #将结果存放到对象self.dataTemplate中
        #最后，返回一个过了规定时间还未更改strField的值的字段集合

        listNewResultFind = []

        if (len(listResult) == 0):
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("无数据需要处理", 'runLog')
        else:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent((("休眠" + str(self.intSleepTime) + "秒~\n") + "..."), 'runLog')
            
            time.sleep(self.intSleepTime)
            #listNewResultFind = []
            
            doMySql = DoMysql(dictMsgForMysql)
            objConnection2 = doMySql.connectionMySQL()
            
            for dictInListItem in listResult:
                intShopId = dictInListItem.get(self.strFieldCompare1)
                intStudentId = dictInListItem.get(self.strFieldCompare2)
                intId = dictInListItem.get(self.strFieldCompare3)
                try:
                    with objConnection2.cursor() as cursor:
                        strSearchIntNextSql = (("SELECT " + self.strField + " FROM " + self.strTable +
                                               " WHERE " + self.strFieldCompare1 + " = %d AND "
                                                + self.strFieldCompare2 + " = %d AND " +
                                                self.strFieldCompare3 + " = %d") %(intShopId, intStudentId, intId))
                        #print(strSearchIntNextSql)
                        cursor.execute(strSearchIntNextSql)
                        listInListItemResult = cursor.fetchall()
                        
                        dictItemField = listInListItemResult[0]
                        #print(dictItemField)
                        intFieldValue = dictItemField.get(self.strField)
                        if (intFieldValue == self.intNext):
                            if(self.fileUtil.boolWhetherShowLog & True):
                                self.fileUtil.writerContent(((self.strFieldCompare1 + " = %d, " +
                                                         self.strFieldCompare2 + "= %d及" + self.strFieldCompare3
                                                              + " = %d的已经更改") %(intShopId, intStudentId,
                                                                                intId)), 'runLog')
                            
                        else:
                            listNewResultFind.append(dictInListItem)
                            if(self.fileUtil.boolWhetherShowLog & True):
                                
                                self.fileUtil.writerContent(((self.strFieldCompare1 + " = %d, " +
                                                         self.strFieldCompare2 + "= %d及" + self.strFieldCompare3 +
                                                              " + %d的还未更改" + self.strField +
                                                              " = %d") %(intShopId, intStudentId, intId, 
                                                                                    intFieldValue)), 'runLog')

                        cursor.close()
                finally:
                    if objConnection2._closed:
                        if(self.fileUtil.boolWhetherShowLog & True):
                            self.fileUtil.writerContent("第二次查询连接意外关闭", 'runLog')

            objConnection2.close()
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("第二次查询连接已正常关闭", 'runLog')
            strResultItem = ""
            if(len(listNewResultFind) == 0):
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent((("所有" + self.strField + "的值已经更改为%d") %(self.intNext)),
                                                'runLog')
            else:
                strContent = ((doMySql.strDatabase + "数据库中,  " + str(intTime) +
                               "秒后，还有如下" + str(len(listNewResultFind)) + "条字段的" + self.strField +
                               "值依然是%d") %(self.intFirst))
                
                for listNewResultItem in listNewResultFind:
                    strResultItem += str(listNewResultItem) + "\n"
                
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(strContent, 'runLog')
                    self.fileUtil.writerContent(strResultItem, 'runLog')

                intNoSendNum = len(listNewResultFind)
                strContent = "> - 未推送总数: " + str(intNoSendNum) + "条\n"
                self.dataTemplate.dataAll += strContent
            
        return listNewResultFind

    def getMsgForCheckLetter(self, dictNeedRunMsg):

        #获取检测数据库字段所需的数据，并判断是否完全
        #返回一个dict类型的数据
        #存放的字段有
        #table_name
        #field_name
        #fieldcompare_name1
        #fieldcompare_name2
        #fieldcompare_namevalue
        #first_field_value
        #next_field_value
        #sleeptime

        dictMsgForCheckLetter = {}

        for keyItem in dictNeedRunMsg:
            if((keyItem == 'table_name') | (keyItem == 'field_name') |
               (keyItem == 'fieldcompare_name1') | (keyItem == 'fieldcompare_name2') |
               (keyItem == 'fieldcompare_name3') | (keyItem == 'fieldcompare_name4') |
               (keyItem == 'fieldcompare_namevalue') | (keyItem == 'first_field_value') |
               (keyItem == 'next_field_value') | (keyItem == 'sleeptime') |
               (keyItem == 'fieldcompare_name3')):
                if(dictNeedRunMsg.get(keyItem) != ''):
                    
                    dictMsgForCheckLetter[keyItem] = dictNeedRunMsg.get(keyItem)
                else:
                    dictMsgForCheckLetter.clear()
                    dictMsgForCheckLetter['err'] = "Msg Incomplete"
                    break
                
        return dictMsgForCheckLetter


    def getNoSendMsgYesterday(self, dictMsgForMysql):

        #从数据库中获取前一天未发送消息的字段,存放到一个list集合
        #dictMsgForMysql: 连接数据库所需的信息
        #返回一个list集合

        listNoSend = []

        dateYesterday = self.runTime.getPastDataDay(1)
        intYesterdayStamp = self.runTime.getTimeStamp(str(dateYesterday), "%Y-%m-%d")
        intTodayStamp = self.runTime.getTodayStamp()

        doMySql = DoMysql(dictMsgForMysql)
        objConnection3 = doMySql.connectionMySQL()

        if objConnection3 is None:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("数据库查询未推送连接失败", 'runLog')
        else:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("数据库查询未推送连接成功", 'runLog')
                self.fileUtil.writerContent("查找" + str(dateYesterday) + "未推送的字段信息",'runLog')
            try:
                with objConnection3.cursor() as cursor:
                    strSearchNoSend = (("SELECT " + self.strFieldCompare1 + " , " + self.strFieldCompare2 +
                    " , " + self.strFieldCompare3 + " FROM " + self.strTable + " WHERE " + self.strField +
                    " = %d " + " AND " + self.strFieldCompare4 + " >= %d AND " +
                    self.strFieldCompare4 + " <= %d") %(self.intFirst, intYesterdayStamp, intTodayStamp))

                    cursor.execute(strSearchNoSend)
                    listNoSend = cursor.fetchall()

                    cursor.close()

            finally:

                if objConnection3._closed:
                    if(self.fileUtil.boolWhetherShowLog & True):
                        self.fileUtil.writerContent("查询未推送数据连接意外关闭", 'runLog')
                else:
                    objConnection3.close()
                    if(self.fileUtil.boolWhetherShowLog & True):
                        self.fileUtil.writerContent("查询未推送数据连接已正常关闭", 'runLog')

            if(len(listNoSend) == 0):
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("未查找到" + str(dateYesterday) + "未推送的字段信息"), 'runLog')
            else:
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("查找到%d条数据未发送" %(len(listNoSend))), 'runLog')
        
        return listNoSend


    def getAlreadySendNumYesterday(self, dictMsgForMysql):

        #获取前一天已经发送推送的个数
        #dictMsgForMysql: 连接数据库所需的信息
        #返回一个int类型

        listAlreadySend = []
        intAlreadySendNum = 0

        dateYesterday = self.runTime.getPastDataDay(1)
        intYesterdayStamp = self.runTime.getTimeStamp(str(dateYesterday), "%Y-%m-%d")
        intTodayStamp = self.runTime.getTodayStamp()

        doMySql = DoMysql(dictMsgForMysql)
        objConnection4 = doMySql.connectionMySQL()

        if objConnection4 is None:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("数据库查询已推送连接失败", 'runLog')
        else:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("数据库查询已推送连接成功", 'runLog')
                self.fileUtil.writerContent("查找" + str(dateYesterday) + "已推送的字段信息",'runLog')
            try:
                with objConnection4.cursor() as cursor:

                    strSearchAlreadySend = (("SELECT COUNT(" + self.strField + ") FROM " + self.strTable +
                    " WHERE " + self.strField + " = %d AND " + self.strFieldCompare4 + " >= %d AND " +
                    self.strFieldCompare4 + " <= %d") %(self.intNext, intYesterdayStamp, intTodayStamp))

                    cursor.execute(strSearchAlreadySend)

                    listAlreadySend = cursor.fetchall()
                    cursor.close()
            finally:

                if objConnection4._closed:
                    if(self.fileUtil.boolWhetherShowLog & True):
                        self.fileUtil.writerContent("查询已推送数据连接意外关闭", 'runLog')
                else:
                    objConnection4.close()
                    if(self.fileUtil.boolWhetherShowLog & True):
                        self.fileUtil.writerContent("查询已推送数据连接已正常关闭", 'runLog')

            if(len(listAlreadySend) == 0):
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("未查找到" + str(dateYesterday) + "已推送的字段信息"), 'runLog')
            else:

                dictItem = listAlreadySend[0]
                intAlreadySendNum = int(dictItem.get("COUNT(" + self.strField + ")"))
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("查找到%d条数据已发送" %(intAlreadySendNum)), 'runLog')


        return intAlreadySendNum


    def getMsgForMysql(self, dictNeedRunMsg):

        #获取连接mysql数据库所需要的数据，并判断是否完全
        #返回一个dict类型的数据
        #存放的字段
        #host
        #port
        #user
        #passwd
        #database

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

        
