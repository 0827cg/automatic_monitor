#!/usr/bin/python3
#coding=utf-8

from monitorbin.util.process import ProcessCL

#author: cg错过
#time: 2017-11-01

class DiskSizeCheck:

    #服务器硬盘容量检测模块

    def __init__(self, fileUtilObj):

        self.fileUtilObj = fileUtilObj


    def checkMountPoing(self, strMountPoingName):

        
