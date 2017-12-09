#!/usr/bin/python3
#coding=utf-8

from monitorbin.util.process import ProcessCL

#author: cg错过
#time: 2017-12-06

class Pm2Operate:

    def __init__(self, intDateMin, intMintHour, fileUtilObj):

        #intDateMin: 当前运行脚本的分钟数
        #intMintHour: 配置文件中设置的时间(分钟数)
        #fileUtilObj: FileUtil的对象(脚本从运行到结束都只有这一个FileUtil对象)

        self.intDateMin = intDateMin
        self.intMintHour = intMintHour
        self.fileUtilObj = fileUtilObj

        if(self.fileUtilObj.boolWhetherShowLog & True):
            self.fileUtilObj.writerContent("-->准备检测pm2", 'runLog')


    def checkPm2(self):

        
        
