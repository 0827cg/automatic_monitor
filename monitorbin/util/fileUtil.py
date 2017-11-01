#!/usr/bin/python3
#coding=utf-8

import os
import xml.dom.minidom
import configparser
from monitorbin.util.sysTime import RunTime

#author: cg错过
#time: 2017-09-30

class FileUtil:

    #文件及部分数据处理类

    configurePath = 'conf'
    configureFileName = 'monitor.conf'

    def __init__(self):

        self.strLogPath = self.getLogPath()
        strWhetherShowLog = self.getWhetherShowLog()
        if(strWhetherShowLog == 'yes'):
            self.boolWhetherShowLog = True
            print("showdebuglog值为yes,将打印输出到log文件")
        else:
            self.boolWhetherShowLog = False
            print("showdebuglog值为no,将不显示输出")
        #strLogPath = self.getLogPath()
        self.setAttribute()

    def setAttribute(self):

        #设置一些属性
        
        runTime = RunTime()
        self.strDateTime = runTime.getDateTime()
        self.strHourTime = runTime.getHourTime()
        self.strDayTime = runTime.getNumDayTime()
        self.strMinTime = runTime.getMinTime()
        self.strHourMinTime = runTime.getHourMinTime()
        self.strNumSecondTime = runTime.getNumSecondTime()
        self.strNumHourTime = runTime.getNumHourTime()

        print(self.strDateTime)

        strlogContentSecondName = "monitor_content-" + self.strNumSecondTime + ".txt"
        strlogContentName = "monitor_content-" + self.strNumHourTime + ".txt"
        strlogErrName = "monitor_err-" + self.strNumHourTime + ".txt"
        strlogErrSecondName = "monitor_err-" + self.strNumSecondTime + ".txt"
        strRunLogName = "monitor_log-" + self.strDayTime + ".txt"
        
        self.strlogContentSecondName = self.strLogPath + '/' + strlogContentSecondName
        self.strlogContentName = self.strLogPath + '/' + strlogContentName
        self.strlogErrName = self.strLogPath + '/' + strlogErrName
        self.strlogErrSecondName = self.strLogPath + '/' + strlogErrSecondName
        self.strRunLogPathName = self.strLogPath + '/' + strRunLogName
        

    def writerContent(self, strContent, strFileMark='Hour', whetherAdd=True):
        
        #strFileMark: 区分写入小时执行的文件还是分钟执行的文件
        #strContent: 写入文件的内容
        #whetherAdd: 是否在文件后面换行追加，默认True
        
        if(strFileMark == 'Hour'):
            if(whetherAdd & True):
                fileObj = open(self.strlogContentName, 'a')
                fileObj.write(strContent + "\n")
                fileObj.close()
            else:
                fileObj = open(self.strlogContentName, 'w')
                fileObj.write(strContent)
                fileObj.close()
        elif(strFileMark == 'Second'):
            if(whetherAdd & True):
                fileObj = open(self.strlogContentSecondName, 'a')
                fileObj.write(strContent + "\n")
                fileObj.close()
            else:
                fileObj = open(self.strlogContentSecondName, 'w')
                fileObj.write(strContent)
                fileObj.close()
        else:
            if(whetherAdd & True):
                fileObj = open(self.strRunLogPathName, 'a')
                fileObj.write(strContent + "\n")
                fileObj.close()
            else:
                fileObj = open(self.strRunLogPathName, 'w')
                fileObj.write(strContent)
                fileObj.close()

    def writerErr(self, strContent, strFileMark='Hour', whetherAdd=True):

        #编写附件，即将操作异常的输出写入到monitor_err...txt文件中

        if(strFileMark == 'Hour'):
            if(whetherAdd & True):
                fileObj = open(self.strlogErrName, 'a')
                fileObj.write("\n" + strContent)
                fileObj.close()
            else:
                fileObj = open(self.strlogErrName, 'w')
                fileObj.write(strContent)
                fileObj.close()
        else:
            if(whetherAdd & True):
                fileObj = open(self.strlogErrSecondName, 'a')
                fileObj.write("\n" + strContent)
                fileObj.close()
            else:
                fileObj = open(self.strlogErrSecondName, 'w')
                fileObj.write(strContent)
                fileObj.close()
            
    

    def getXMLTagElementValue(self, strFilePath, strTagName, strTagElementName, intTagIndex):

        #获取xml文件指定标签的内容，返回一个字符串值
        #self: 对象本身
        #strTagName: 标签名字
        #strTagElementName: 标签中的元素名字
        #intTagIndex: 文件中出现该标签的序列号(即第几个，从0开始)
        
        confObj = xml.dom.minidom.parse(strFilePath)

        documentElementObj = confObj.documentElement
        listElementItem = documentElementObj.getElementsByTagName(strTagName)
        #按照顺序存放，文件内容中第一个出现该标签名字的就放在集合的下标为0的位置
        tagElement = listElementItem[intTagIndex]
        strTagElementValue = tagElement.getAttribute(strTagElementName)
        if(self.boolWhetherShowLog & True):
            print(strTagElementName + "=" + strTagElementValue)
        return strTagElementValue


    def getConfFileValue(self, configParserObj, configureFileNameAndPath):

        #获取conf后缀的配置文件内容，返回一个字典
        #注释了不读取，值为空会读取
        #configParserObj: 读取配置文件的对象
        #configureFileNameAndPath: 配置文件路径
        #读取写入的key名字全部小写

        dictConfMsg = {}
        intMark = self.checkFileExists(configureFileNameAndPath)
        if(intMark == 1):
            configParserObj.read(configureFileNameAndPath)
            try:
                listSectionName = configParserObj.sections()
            except:
                if(self.boolWhetherShowLog & True):
                    self.writerContent("读取配置文件出错", 'runLog')
            else:
                for sectionItem in listSectionName:
                    #print(sectionItem)
                    listKeyName = configParserObj.options(sectionItem)
                    #print(listKeyName)
                    sectionObj = configParserObj[sectionItem]
                    if(len(listKeyName) != 0):
                        for keyItem in  listKeyName:
                            valueItem = sectionObj[keyItem]
                            if(valueItem == None):
                                dictConfMsg[sectionItem] = listKeyName
                            else:
                                dictConfMsg[keyItem] = valueItem
                    else:
                        dictConfMsg[sectionItem] = ''
        #print(dictConfMsg)
        return dictConfMsg


    def readFileContent(self, inputFileName):

        #读取普通文件内容并返回
        
        fileObj = open(inputFileName, 'r')
        strFileContent = fileObj.read()
        fileObj.close()
        
        return strFileContent


    def initConfigureFile(self):
        
        #初始化配置文件

        strTomcatPath = "/home/liying/dev/tomcat-7.0.73"
        strNginxPath = "/usr/local/nginx"
        strRedisPath = "/home/liying/dev/redis-2.8.24"

        strServerName = "116"
        strUserName = "林繁"

        strLogPath = "logs"

        strSmtp_server = "smtp.qq.com"
        strEmail_sendAddr = "yakult-cg@qq.com"
        strEmail_sendPasswd = "lscgsbnjddtgdegc"
        
        strToEmail = "1732821152@qq.com"
        #strToEmail2 = "1732821152@qq.com"

        strAuthor = "cg错过"
        strCreateTime = "2017-09-30"

        strIntervals = "300"
        strMinute = "30"
        strLogTime = "11:50"
        strShowLog = "no"

        if not os.path.exists(self.configurePath):
            os.mkdir(self.configurePath)

        configureFileNameAndPath = self.configurePath + '/' + self.configureFileName

        config = configparser.ConfigParser(allow_no_value=True, delimiters=':')
        config.add_section('ProjectConfigure')
        config.add_section('UseConfigure')
        config.add_section('LogConfigure')
        config.add_section('EmailConfigure')
        config.add_section('ToEmail')
        config.add_section('RunConfigure')
        config.add_section("Message")

        config.set('ProjectConfigure', '# tomcat root path')
        config.set('ProjectConfigure', 'tomcatpath', strTomcatPath)
        config.set('ProjectConfigure', 'nginxpath', strNginxPath)
        config.set('ProjectConfigure', 'redispath', strRedisPath)

        config.set('UseConfigure', '# computer system nickname by youself')
        config.set('UseConfigure', 'servername', strServerName)
        config.set('UseConfigure', '# set nickname to send email')
        config.set('UseConfigure', 'username', strUserName)

        config.set('LogConfigure', '# set file path to save log files')
        config.set('LogConfigure', 'logpath', strLogPath)

        config.set('EmailConfigure', '# set smtp_server address')
        config.set('EmailConfigure', 'smtp_server', strSmtp_server)
        config.set('EmailConfigure', '# set mail address to send email')
        config.set('EmailConfigure', 'email_sendAddr', strEmail_sendAddr)
        config.set('EmailConfigure', '# set authorization code for mail address to send email')
        config.set('EmailConfigure', 'email_sendPasswd', strEmail_sendPasswd)

        config.set('ToEmail', '# this to add mail address to accept email')
        config.set('ToEmail', strToEmail)
        #config.set('ToEmail', strToEmail2)

        config.set('RunConfigure', '# set run progress timing, unit second')
        config.set('RunConfigure', 'run_intervals', strIntervals)
        config.set('RunConfigure', '# set when minute in every hour to check project, unit minute')
        config.set('RunConfigure', 'when_minute_in_hour', strMinute)
        config.set('RunConfigure', '# set time to remove log files unit 24 hour time. like HH:MM')
        config.set('RunConfigure', 'remove_log_time', strLogTime)
        config.set('RunConfigure', '# set whether show run debug logs in log files, value yes or no')
        config.set('RunConfigure', 'showDebugLog', strShowLog)

        config.set('Message', 'author', strAuthor)
        config.set('Message', 'createtime', strCreateTime)

        with open(configureFileNameAndPath, 'w') as configureFile:
            config.write(configureFile, space_around_delimiters=True)

        #print("done")


    def getNeedRunMsg(self):

        #根据配置文件的配置内容来选择代码执行
        #即从存放的字典中去除不需要检测运行的项目(未配置值的参数)，之后返回
        if(self.boolWhetherShowLog & True):
            self.writerContent(("============" + self.strDateTime + "============"), 'runLog')
            self.writerContent("获取运行需要的配置数据", 'runLog')
        
        #fileUtil = FileUtil()
        dictNewConfMsg = {}
        dictConfMsg = self.readConfigureFile()
        intMark = self.checkConfMsg(dictConfMsg)
        if(intMark == 1):
            intTomcatMark = self.checkRunProject("tomcat", "tomcatpath", dictConfMsg)
            if(intTomcatMark == 0):
                del dictConfMsg['tomcatpath']

            intNginxMark = self.checkRunProject("nginx", "nginxpath", dictConfMsg)
            if((intNginxMark == 0)):
                del dictConfMsg['nginxpath']

            intRedisMark = self.checkRunProject("redis", "redispath", dictConfMsg)
            if(intRedisMark == 0):
                del dictConfMsg['redispath']
            dictNewConfMsg = dictConfMsg
        elif(intMark == 0):
            dictNewConfMsg['0'] = 'error'
            
        if(self.boolWhetherShowLog & True):
            self.writerContent("需要运行的有: ", 'runLog')
            self.writerContent(str(dictNewConfMsg), 'runLog')
        return dictNewConfMsg


    def readConfigureFile(self):

        #读取脚本配置文件
        dictConfMsgTotal = {}
        configureFileNameAndPath = self.configurePath + '/' + self.configureFileName
        self.checkAndInitConfigure(configureFileNameAndPath)
        config = configparser.ConfigParser(allow_no_value=True, delimiters=':')
        dictConfMsg = self.getConfFileValue(config, configureFileNameAndPath)
        dictConfMsgTotal.update(dictConfMsg)
        if(len(dictConfMsgTotal)  == 0):
            if(self.boolWhetherShowLog & True):
                self.writerContent("未获取到配置文件内容", 'runLog')
        if(self.boolWhetherShowLog & True):
            self.writerContent("读取到的配置文件信息如下: ", 'runLog')
            self.writerContent(str(dictConfMsgTotal), 'runLog')

        return dictConfMsgTotal

    def checkConfMsg(self, dictConfMsg):

        #检测配置文件是否完全
        #其中日志路径和email值必须存在
        #所以这里只检查logpath和email
        #email仅包括smtp_server, email_sendaddr, email_sendpasswd

        #2017-10-30添加了run_intervals, when_minute_in_hour, remove_log_time
        
        intMark = -1
        if(len(dictConfMsg) != 0):
            for keyItem in dictConfMsg:
                if((keyItem == 'logpath') | (keyItem == 'smtp_server') | (keyItem == 'email_sendaddr')
                  | (keyItem == 'email_sendpasswd') | (keyItem == 'run_intervals')
                   | (keyItem == 'when_minute_in_hour') | (keyItem == 'remove_log_time')):
                    if(dictConfMsg.get(keyItem) == ''):
                        strErr = ("未读取到%s配置参数的值，请修改配置文件" %(keyItem))
                        self.writerContent(strErr, 'runErr')
                        intMark = 0
                        break
                    else:
                        intMark = 1
        else:
            self.writerContent("未读取到配置文件内容", 'runLog')
        return intMark
           


    def checkRunProject(self, projectName, strKey, dictConfMsg):

        #根据配置文件的配置，判断并选择代码块来执行
        #如果返回值为1，则表示返回允许执行检测projectName这个项目

        intMark = -1
        if(strKey in dictConfMsg):
            if(dictConfMsg.get(strKey) != ''):
                intMark = 1
            else:
                intMark = 0
                strErr = ("未读取到%s配置参数,如需检测%s请修改配置文件" %(projectName, projectName))
                self.writerContent(strErr, 'runLog')
        return intMark


    def checkFileExists(self, configureFileNameAndPath):

        #检测配置文件是否存在，不存在则返回-1

        intMark = -1
        if(os.path.exists(configureFileNameAndPath)):
            intMark = 1

        return intMark

    def checkAndInitConfigure(self, configureFileNameAndPath):

        #检测并初始化配置文件

        intMark = self.checkFileExists(configureFileNameAndPath)
        if(intMark != 1):
            print("配置文件monitor.conf不存在,脚本自动创建并初始化")
            print("配置文件monitor.conf路径为" + self.configurePath + "/"
                                   + self.configureFileName)
            #self.writerContent("配置文件monitor.conf不存在,脚本自动创建并初始化", 'runErr')
            #strErr = ("配置文件monitor.conf路径为" + self.configurePath + "/" + self.configureFileName)
            #self.writerContent(strErr, 'runErr')
            self.initConfigureFile()

    def checkAndCreate(self, FileNameAndPath):

        #检测并创建日志文件路径

        intMark = self.checkFileExists(FileNameAndPath)
        if(intMark != 1):
            if(self.boolWhetherShowLog & True):
                self.writerContent("配置的日志文件夹路径不存在，脚本执行自动创建", 'runLog')
            #self.writerContent("配置的日志文件夹路径不存在，脚本执行自动创建", 'runErr')
            os.mkdir(FileNameAndPath)

    def getLogPath(self):
        
        #获取配置文件中存放日志文件路径

        strLogPath = ''
        configureFileNameAndPath = self.configurePath + '/' + self.configureFileName
        self.checkAndInitConfigure(configureFileNameAndPath)
        config = configparser.ConfigParser(allow_no_value=True, delimiters=':')
        config.read(configureFileNameAndPath)
        if(config.has_section('LogConfigure')):
            strLogPath = config['LogConfigure']['logpath']
            self.checkAndCreate(strLogPath)
        else:
            self.writerContent("配置文件内容缺少logpath配置参数", 'runLog')
            #self.writerContent("配置文件内容缺少日志配置参数", 'runErr')
        return strLogPath


    def getWhetherShowLog(self):

        #获取配置文件中是否打开debug输出到log文件中
        #如果配置文件中的showdebuglog值为空或者不等于'yes','no',则都将起设置为'no'
        #也就是默认为no

        strWhetherShowLog = ''
        configureFileNameAndPath = self.configurePath + '/' + self.configureFileName
        self.checkAndInitConfigure(configureFileNameAndPath)
        config = configparser.ConfigParser(allow_no_value=True, delimiters=':')
        config.read(configureFileNameAndPath)
        if(config.has_section('RunConfigure')):
            strWhetherShowLog = config['RunConfigure']['showdebuglog']
        else:
            self.writerContent("配置文件内容缺少showdebuglog配置参数", 'runLog')
            #self.writerContent("配置文件内容缺少日志配置参数", 'runErr')
        if((strWhetherShowLog != 'yes') & (strWhetherShowLog != 'no')):
            strWhetherShowLog = 'no'
        return strWhetherShowLog
        

    def reWriterForEmail(self, listSendContent, dictEmailMsg):

        #重构需要邮件发送的内容，并设置对应主题，并返回list
        #重构后的list数据集合格式：无错误日志list长度为3，有错误日志list长度为4
        #list[0]: Hour或者Second或者no
        #list[1]: 邮件主题
        #list[2]: 需要发送的邮件内容(已重构的内容)
        #list[3]: 错误日志的相对路径地址

        strNewContent = ''
        strContent = listSendContent[1]

        strServerName = 'none'
        strUserName = 'cg'
        for keyItem in dictEmailMsg:
            if((keyItem == 'servername') | (keyItem == 'username')):
                if(keyItem == 'servername'):
                    strServerName = dictEmailMsg.get('servername')
                else:
                    strUserName = dictEmailMsg.get('username')
            else:
                continue

        strContentLine = "===================="

        strNewContent = strContent[:0] + strContentLine + "\n" + strContent[0:]
        strNewContent = (strNewContent + "\n" + strContentLine + "\n" + "---" +
                         strUserName + "\n" + "---" + self.strDateTime)

        listSendContent[1] = strNewContent
        if(listSendContent[0] == 'Hour'):
            strSubject = strServerName + "今日" + self.strHourTime + "时执行结果"
            listSendContent.insert(1, strSubject)
        elif(listSendContent[0] == 'Second'):
            strSubject = strServerName + "今日" + self.strHourMinTime + "时检测到异常"
            listSendContent.insert(1, strSubject)        

        else:
            strSubject = strServerName + "脚本运行异常"
            listSendContent.insert(1, strSubject)
        if(self.boolWhetherShowLog & True):    
            self.writerContent("数据已重构, 如下", 'runLog')
            self.writerContent(str(listSendContent), 'runLog')
        return listSendContent

        

