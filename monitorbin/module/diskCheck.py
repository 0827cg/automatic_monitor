# -*- coding: utf-8 -*-

from monitorbin.util.process import ProcessCL

#author: cg错过
#time: 2017-12-07

class DiskSizeCheck:

    intOverAllCheckNum = 0

    #服务器硬盘容量检测模块

    def __init__(self, fileUtilObj, dataTempObj, dictNeedRunMsg, intHourTime, intHourCheckAll, intWarningLevel,
                 allModuleRunAllObj):

        self.fileUtil = fileUtilObj
        self.processCL = ProcessCL()
        self.intHourTime = intHourTime
        self.intHourCheckAll = intHourCheckAll
        self.intWarningLevel = intWarningLevel
        self.dataTempObj = dataTempObj
        self.allModuleRunAllObj = allModuleRunAllObj

        if('servername' in dictNeedRunMsg):
            self.strServerName = dictNeedRunMsg.get('servername')
        else:
            self.strServerName = ""

        self.checkDisk()

    def checkDisk(self):

        #检测disk
        #分时间执行,每天出一个磁盘概况，其余监控磁盘，出现超过的时候就提醒

        strAllMsgForLog = str(self.getAllMsg())
        if(self.fileUtil.boolWhetherShowLog & True):
            self.fileUtil.writerContent("-->开始检测磁盘空间", 'runLog')
            self.fileUtil.writerContent("得到的信息如下:", 'runLog')
            self.fileUtil.writerContent(strAllMsgForLog, 'runLog')
        
        if((self.intHourTime == self.intHourCheckAll) or (self.intHourTime == ("0" + self.intHourCheckAll))):
            
            #strAllMsg = self.getAllMsg()
            #print(strAllMsg)
            if(self.allModuleRunAllObj.intOverAllCheckDiskNum == 0):
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent("将检测磁盘全部节点信息", 'runLog')
                
                intMountPointsNum = self.getMountPointsNum()
                listMountPointsMsg = self.getMountPointsMsg(intMountPointsNum)
                listCutMountPointsMsg = self.formatCutMsgForSendAll(listMountPointsMsg)
                strCutAllMsg = self.formatCutMsgForSendAllToStr(listCutMountPointsMsg)
                
                self.dataTempObj.dataAll += ("> - " + self.strServerName +
                                             "系统各节点空间使用量如下: \n" + "\n> " + strCutAllMsg)

                self.allModuleRunAllObj.intOverAllCheckDiskNum = 1
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("今日检测磁盘次数已标记为" +
                                                 str(self.allModuleRunAllObj.intOverAllCheckDiskNum)), 'runLog')
                
            else:
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("今日" + str(self.intHourCheckAll) +
                                                "内已检测硬盘,今日将不再检测\n" +
                                                 "将进行错误监控任务"), 'runLog')
                self.checkTog()
            
        else:

            self.checkTog()

            '''
            intMountPointsNum = self.getMountPointsNum()
            listMountPointsMsg = self.getMountPointsMsg(intMountPointsNum)
            listOutMsg = self.checkUse(listMountPointsMsg)
            if(len(listOutMsg) > 0):
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("超过" + str(self.intWarningLevel) + "%的挂载点如下:"), 'runLog')
                    self.fileUtil.writerContent(str(listOutMsg), 'runLog')
                self.dataTempObj.dataAll += "> 超过的节点如下\n" + "> " + listOutMsg
            else:
                if(self.fileUtil.boolWhetherShowLog & True):
                    self.fileUtil.writerContent(("无超过" + str(self.intWarningLevel) + "%的挂载点"), 'runLog')
            '''


    def checkTog(self):

        intMountPointsNum = self.getMountPointsNum()
        listMountPointsMsg = self.getMountPointsMsg(intMountPointsNum)
        listOutMsg = self.checkUse(listMountPointsMsg)
        if(len(listOutMsg) > 0):
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent(("超过" + str(self.intWarningLevel) + "%的挂载点如下:"), 'runLog')
                self.fileUtil.writerContent(str(listOutMsg), 'runLog')
            self.dataTempObj.dataAll += "> 超过的节点如下\n" + "> " + listOutMsg
        else:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent(("无超过" + str(self.intWarningLevel) + "%的挂载点"), 'runLog')



    def getMountPointsNum(self):

        #获取节点个数，根据df -Th命令后的输出，统计行数
        #返回一个int类型数值

        strGetMountPointsNumCL = ("df -Th | wc -l")
        dictResult = self.processCL.getResultAndProcess(strGetMountPointsNumCL)
        intTotalNum = dictResult.get('stdout')
        #print(intTotalNum)
        intMountPointsNum = int(intTotalNum) - 1
        
        return intMountPointsNum



    def getMountPointsMsg(self, intMountPointsNum):

        # 获取各节点的信息
        #intMountPointsNum: 总的节点个数
        #返回一个元素为dict的list集合
        #去除了列名

        listMountPointsMsg = []
        listMsgName = ['filesystem', 'type', 'size', 'used', 'avail', 'use', 'mountedon']

        #上面的数值来自
        '''
        [root@10-9-144-237 ~]# df -Th
        Filesystem     Type   Size  Used Avail Use% Mounted on
        /dev/vda1      ext4    20G  3.8G   15G  21% /
        tmpfs          tmpfs  972M     0  972M   0% /dev/shm
        /dev/vdb       ext4    99G   39G   55G  42% /data
        /dev/vdc1      ext4   493G   61G  408G  13% /data0
        '''
        for pointsNum in range(intMountPointsNum):
            dictOneMountPointsMsg = {}
            for columnNum in range(len(listMsgName)):

                strGetMountPointsMsgCL = ("df -Th | head -n " + str(pointsNum + 2) +
                " | tail -n 1 | awk "+ "'" + "{print $" + str(columnNum + 1) + "}'")
                
                dictResult = self.processCL.getResultAndProcess(strGetMountPointsMsgCL)
                strResultStdout = dictResult.get('stdout')
                
                dictOneMountPointsMsg[listMsgName[columnNum]] = strResultStdout.strip('\n')
                
            listMountPointsMsg.append(dictOneMountPointsMsg)
        if(self.fileUtil.boolWhetherShowLog & True):
            self.fileUtil.writerContent(str(len(listMountPointsMsg)) + "条挂载点信息的dict类型显示如下",
                                        'runLog')
        for dictMountPointsMsgItem in listMountPointsMsg:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent(str(dictMountPointsMsgItem), 'runLog')

        return listMountPointsMsg
        

    def checkUse(self, listMountPointsMsg):

        #检测各个节点空间使用量是否超过指定值
        #并将超过指定值的节点信息添加到listOutMsg,并返回

        listOutMsg = []
        for dictMountItem in listMountPointsMsg:
            intUse = int(dictMountItem.get('use').strip('%'))
            if(intUse >= int(self.intWarningLevel)):
                listOutMsg.append(dictMountItem)

        return listOutMsg
        

    def getAllMsg(self):

        #为每隔一大段时间，检测得到各个节点的所有概况信息

        strGetAllMsgCL = ("df -Th")
        dictAllMsg = self.processCL.getResultAndProcess(strGetAllMsgCL)
        strAllMsg = dictAllMsg.get('stdout')

        return strAllMsg


    def formatCutMsgForSendAll(self, listMountPointsMsg):

        #格式化并切割出部分数据，用提供给钉钉发送
        #返回一个存放元素未list的list集合
        #例如
        #[['mounton', 'used', 'use'], ['/', '11G', '51%'], ['/dev', '0', '0%'], ['/dev/shm', '0', '0%'],,,,]
        #listMountPointsMsg: 表示

        listCutMountPointsMsgName = ['mounton', 'used', 'use']
        listCutMountPointsMsg = []
        listCutMountPointsMsg.append(listCutMountPointsMsgName)
        for dictMountPointsMsgItem in listMountPointsMsg:
            listCutMountPointsMsgValue = []
            listCutMountPointsMsgValue.append(dictMountPointsMsgItem.get('mountedon'))
            listCutMountPointsMsgValue.append(dictMountPointsMsgItem.get('used'))
            listCutMountPointsMsgValue.append(dictMountPointsMsgItem.get('use'))
            listCutMountPointsMsg.append(listCutMountPointsMsgValue)

        if(self.fileUtil.boolWhetherShowLog & True):
            self.fileUtil.writerContent("抽取出来的磁盘概况如下:", 'runLog')

        for listCutMountPointMsgItem in listCutMountPointsMsg:
            if(self.fileUtil.boolWhetherShowLog & True):
                self.fileUtil.writerContent((str(listCutMountPointMsgItem) + "\n"), 'runLog')

        return listCutMountPointsMsg


    def formatCutMsgForSendAllToStr(self, listCutMountPointsMsg):

        #同样时格式话，不过参数时经过切割后的数据
        #listCutMountPointsMsg: 表示切割出的部分数据,由formatCutMsgForSendAll()方法获得
        #返回一个带有部分格式的字符串类型数据

        strMsgForSendAll = ""

        for listCutMountPointsMsgItem in listCutMountPointsMsg:
            strMsgForSendAll += "\t\t "
            for index in range(3):
                strMsgForSendAllLine = listCutMountPointsMsgItem[index]
                strMsgForSendAll += strMsgForSendAllLine + "\t\t"
            strMsgForSendAll += "\n"

        return strMsgForSendAll

        
