#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from monitorbin.util.process import ProcessCL

# author: cg错过
# time: 2018-03-01


class ProjectCheck:

    # 用来重启pm2搭载的项目，类内部不写调用重启的代码，全靠外部调用

    def __init__(self, fileUtilObj):

        self.fileUtilObj = fileUtilObj
        self.processCL = ProcessCL()

    def restartProByStrName(self, strProName):

        # 依照项目名来重启项目
        # strProName: pm2搭载项目名
        # 有返回值，int类型，1表示重启成功，0表示重启失败

        intResult = -1
        strRestartProCL = ("pm2 restart " + strProName)

        dictCLResult = self.processCL.getResultAndProcess(strRestartProCL)
        strProErr = dictCLResult['stderr']
        if strProErr == '':
            self.fileUtilObj.writerContent(("项目" + strProName + "已重启成功"), 'runLog')
            intResult = 1
        else:
            self.fileUtilObj.writerContent(("项目" + strProName + "重启出错"), 'runLog')
            intResult = 0

        return intResult


    def restartProByListName(self, listProName):

        # 依照项目名来重启项目
        # listProName: 存放pm2搭载项目名的list集合
        # 此方法暂时用不到

        for index in range(len(listProName)):
            self.restartProByListName(listProName[index])



