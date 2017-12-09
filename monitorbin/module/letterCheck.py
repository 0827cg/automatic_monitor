#!/usr/bin/python3
#coding=utf-8

#author: cg错过
#time: 2017-12-08

from monitorbin.util.mysqlConnect import DoMysql
import time


class CheckLetter:

    #检测数据库表中某个字段

    def __init__(self, fileUtilObj, dataTemplateObj, dictNeedRunMsg):

        self.fileUtil = fileUtilObj
        self.dataTemplate = dataTemplateObj

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
            self.strFieldCompareValue = dictMsgForCheckLetter.get('fieldcompare_namevalue')
            self.intFirst = int(dictMsgForCheckLetter.get('first_field_value'))
            self.intNext = int(dictMsgForCheckLetter.get('next_field_value'))
            self.intSleepTime = int(dictMsgForCheckLetter.get('sleeptime'))
            
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent(("-->执行检测数据库字段" + self.strField + "任务"), 'runLog')

            self.checkRun(dictMsgForMysql)


    def checkRun(self, dictMsgForMysql):

        #执行检测
        #这个检测数据库字段并未分时间段
        #其他的项目检测就分了大任务和小任务检测，即按时和按分检测
        #这个就没有，因为数据库中的字段都是时刻在变化

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
                self.fileUtil.writerContent("数据库链接失败", 'runLog')
        else:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("数据库连接成功", 'runLog')
                self.fileUtil.writerContent((("查找" + self.strField + "值为%d" + "的数据") %(self.intFirst)),
                                            'runLog')

            try:
                with objConnection.cursor() as cursor:
                    strSearchSql = ("SELECT " + self.strFieldCompare1 + " , " + self.strFieldCompare2 +
                                    " FROM " + self.strTable + " WHERE " + self.strField + "= %d AND " +
                                    self.strFieldCompareValue + " != " + "'" + "'" + " AND " +
                                    self.strFieldCompareValue + " IS NOT NULL" + " AND " +
                                    self.strFieldCompareValue + " != " + "'" + "null" + "'")
                    
                    cursor.execute(strSearchSql %(self.intFirst))
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

        if (len(listResult) == 0):
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent("无数据需要处理", 'runLog')
        else:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent((("休眠" + str(self.intSleepTime) + "秒~\n") + "..."), 'runLog')
            
            time.sleep(self.intSleepTime)
            listNewResult = []
            
            doMySql = DoMysql(dictMsgForMysql)
            objConnection2 = doMySql.connectionMySQL()
            
            for dictInListItem in listResult:
                intShopId = dictInListItem.get(self.strFieldCompare1)
                intStudentId = dictInListItem.get(self.strFieldCompare2)
                try:
                    with objConnection2.cursor() as cursor:
                        strSearchIntNextSql = (("SELECT " + self.strField + " FROM " + self.strTable +
                                               " WHERE " + self.strFieldCompare1 + " = %d AND "
                                                + self.strFieldCompare2 + " = %d ") %(intShopId, intStudentId))
                        #print(strSearchIntNextSql)
                        cursor.execute(strSearchIntNextSql)
                        listInListItemResult = cursor.fetchall()
                        
                        dictItemField = listInListItemResult[0]
                        #print(dictItemField)
                        intFieldValue = dictItemField.get(self.strField)
                        if (intFieldValue == self.intNext):
                            if(self.fileUtil.boolWhetherShowLog & True):
                                self.fileUtil.writerContent(((self.strFieldCompare1 + " = %d及 " +
                                                         self.strFieldCompare2 +
                                                         "= %d的已经更改") %(intShopId, intStudentId)), 'runLog')
                            
                        else:
                            listNewResult.append(dictInListItem)
                            if(self.fileUtil.boolWhetherShowLog & True):
                                
                                self.fileUtil.writerContent(((self.strFieldCompare1 + " = %d及 " +
                                                         self.strFieldCompare2 + "= %d的还未更改" +
                                                         self.strField + " = %d") %(intShopId, intStudentId,
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
            if(len(listNewResult) == 0):
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent((("所有" + self.strField + "的值已经更改为%d") %(self.intNext)),
                                                'runLog')
            else:
                strContent = ((doMySql.strDatabase + "数据库中,  " + str(intTime) +
                               "秒后，还有如下" + str(len(listNewResult)) + "条字段的" + self.strField +
                               "值依然是%d") %(self.intFirst))
                
                for listNewResultItem in listNewResult:
                    strResultItem += str(listNewResultItem) + "\n"
                
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(strContent, 'runLog')
                    self.fileUtil.writerContent(strResultItem, 'runLog')

                intNoSendNum = len(listNewResult)
                strContent = "> - 未推送总数: " + str(intNoSendNum) + "条\n"
                self.dataTemplate.dataAll += strContent
            
        return listNewResult

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
               (keyItem == 'fieldcompare_namevalue') | (keyItem == 'first_field_value') |
               (keyItem == 'next_field_value') | (keyItem == 'sleeptime')):
                if(dictNeedRunMsg.get(keyItem) != ''):
                    
                    dictMsgForCheckLetter[keyItem] = dictNeedRunMsg.get(keyItem)
                else:
                    dictMsgForCheckLetter.clear()
                    dictMsgForCheckLetter['err'] = "Msg Incomplete"
                    break
                
        return dictMsgForCheckLetter

        


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

        

            

        
        

        
