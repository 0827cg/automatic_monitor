# -*- coding: utf-8 -*-

import subprocess

# author: cg错过
# time: 2017-09-30

class ProcessCL:

    # python操作Linux模块

    def getResultAndProcess(self, strCL):

        # 获取无持续输出的命令操作后的结果，将其分类(stdout和stderr)
        # 获取正常输出和错误输出，存放到dict中返回
        # strCL: 操作的命令
        # 返回的是一个dict集合,key有stdout,stderr
        
        dictResult = {}
        strOut = ''
        strErr = ''
        subObj = subprocess.Popen(strCL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                  universal_newlines=True)
        returnCode = subObj.poll()
        while returnCode is None:
            stdout, stderr = subObj.communicate()
            returnCode = subObj.poll()
            strOut += stdout
            strErr += stderr
        dictResult['stdout'] = strOut
        dictResult['stderr'] = strErr
        
        return dictResult


    def getContinueResultAndProcess(self, strCL):

        # 获取有持续输出的程序的结果，将其分类(stdout和stderr)
        # 但检测到无输出后就退出
        # strCL: 操作的命令
        # 返回的是一个dict集合,key有stdout,stderr
        
        strOut = ''
        strErr = ''
        dictResult = {}
        subObj = subprocess.Popen(strCL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
                                  universal_newlines=True)
        returnCode = subObj.poll()
        while returnCode is None:
            lineOut = subObj.stdout.readline()
            lineErr = subObj.stdout.readline()
            returnCode = subObj.poll()
            lineOut = lineOut.strip()
            lineErr = lineErr.strip()

            strOut += lineOut
            strErr += lineErr
            if((lineOut == '') | (lineErr == '')):
                break
            
        dictResult['stdout'] = strOut
        dictResult['stderr'] = strErr

        return dictResult
