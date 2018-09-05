#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg错过
# time  : 2017-12-07

import urllib.request
import json

class ResponseDD:

    # 将结果发送到钉钉

    def __init__(self, fileUtilObj, dataTemplateObj, dictNeedRunMsg):

        self.fileUtilObj = fileUtilObj
        self.dataTemplate = dataTemplateObj
        dictMsgForDD = self.getForDDMsg(dictNeedRunMsg)

        if (len(dictMsgForDD) == 1) and ('err' in dictMsgForDD):
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("钉钉发送配置不全,发送钉钉消息任务运行中止", 'runLog')
        else:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("-->执行发送钉钉消息任务", 'runLog')
            self.webHookURL = dictMsgForDD.get('webhook')
            strData = self.dataTemplate.dataAll
            if strData == "":
                if self.fileUtilObj.boolWhetherShowLog & True:
                    self.fileUtilObj.writerContent("数据为空,将不执行执行发送钉钉消息任务", 'runLog')
            else:
                if self.fileUtilObj.boolWhetherShowLog & True:
                    self.fileUtilObj.writerContent("发送至钉钉的初始数据内容如下:", 'runLog')
                    self.fileUtilObj.writerContent(strData, 'runLog')
                    
                dictData = self.dataTemplate.createMarkdownData()
                
                if self.fileUtilObj.boolWhetherShowLog & True:
                    self.fileUtilObj.writerContent("重构后的数据内容如下:", 'runLog')
                    self.fileUtilObj.writerContent(str(dictData), 'runLog')
                
                self.sendData(dictData)
                
            

    def getForDDMsg(self, dictNeedRunMsg):

        # 从所有数据中提取出仅用来发送钉钉所需要的数据,并返回
        # dictNeedRunMsg: 存放从配置文件中读取到的数据，其数据是本次检测运行所需要的数据
        # 该数据仅进行了初步过滤
        # 初步这里只需要'webhook'这个数据

        dictMsgForDD = {}
        if 'webhook' in dictNeedRunMsg:
            if dictNeedRunMsg.get('webhook') != '':
                dictMsgForDD['webhook'] = dictNeedRunMsg.get('webhook')
            else:
                dictMsgForDD['err'] = "Msg Incomplete"
                
        return dictMsgForDD



    def sendData(self, dictData):

        # 用来发送消息到钉钉的

        headers = {'Content-Type': 'application/json'}

        json_data = json.dumps(dictData).encode('utf-8')
        req = urllib.request.Request(self.webHookURL, data=json_data, headers=headers)
        response = urllib.request.urlopen(req)
        if int(response.getcode()) == 200:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("已发送至钉钉", 'runLog')
        else:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("未成功发送至钉钉", 'runLog')

        
