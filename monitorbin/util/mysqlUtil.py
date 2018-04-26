#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg错过
# time  : 2018-04-25

from monitorbin.util.mysqlConnect import DoMysql

class MySqlUtil:

    # 数据库操作类

    def __init__(self, fileUtilObj):

        self.fileUtilObj = fileUtilObj

    def doSearchSql(self, strSearchSql, dictMsgForMysql):

        # 执行sql语句,这里用来做查找
        # strSearchSql: 要执行的sql语句
        # dictMsgForMysql: 创建一条数据库连接所需要的数据

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
