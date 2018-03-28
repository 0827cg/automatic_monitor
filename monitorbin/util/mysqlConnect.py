#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg
# time  : 2017-12-04

import pymysql.cursors

class DoMysql:

    # 连接数据库,返回一条连接
    
    def __init__(self, dictMsgForMysql):

        # 构造函数

        self.strHost = dictMsgForMysql.get('host')
        self.strPort = dictMsgForMysql.get('port')
        self.strUser = dictMsgForMysql.get('user')
        self.strPasswd = dictMsgForMysql.get('passwd')
        self.strDatabase = dictMsgForMysql.get('database')
        

    def connectionMySQL(self):

        # 连接数据库
        # 返回一个连接

        connection = pymysql.connect(host = self.strHost, port = int(self.strPort), user = self.strUser,
                                     passwd = self.strPasswd, db = self.strDatabase,
                                     charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)

        return connection
