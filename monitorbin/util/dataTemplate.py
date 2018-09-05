#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg错过
# time  : 2017-12-08

class DataTemplate:

    # data数据模板
    # 程序运行得到的数据将不再存放到txt文件中，而是存放到此模板中，即内存中

    def __init__(self, strDateTime, strServerName):

        # 添加标识self.strServerName-add in 2018-04-09

        self.dataForHour = ""
        self.dataForSecond = ""
        self.dataAll = ""
        self.strDateTime = strDateTime
        self.strServerName = strServerName


    def createDictTextData(self):

        # 创建一个普通的文本dict数据，并返回

        strDataContent = (self.dataAll + "> \r\r " + self.strServerName + '-' + self.strDateTime)
        
        dictData = {
            "msgtype": "text", 
            "text": {
                "content": strDataContent
            }, 
            "isAtAll": 'true'
        }
        return dictData


    def createMarkdownData(self):

        # 创建一个markdown语法的dict数据，并返回

        strDataContentMark = (self.dataAll + "> \r\r " + self.strServerName + '-' + self.strDateTime)

        dictData = {
            "msgtype": "markdown", 
            "markdown": {
                "title": "监控服务",
                "text": "#### [监控服务]\n" + strDataContentMark
            },
            "at": {
                "isAtAll": 'true'
            }
        }
        return dictData


    def createMarkdownDataForEmail(self):

        # 创建一个markdown语法的数据，并返回

        strDataContentMark = (self.dataAll + "> \r\r " + self.strServerName + '-' + self.strDateTime)

        return strDataContentMark
