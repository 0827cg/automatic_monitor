#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg错过
# time  : 2018-01-11

import decimal
from monitorbin.util.sysTime import RunTime
from monitorbin.util.prettyTableDo import PrettyTableDo

class PicArrivalCompare:

    # 前一天和昨天的图片到达率中获取对比设备的签到次数
    # 例如昨天和前天对比后得到：新增机构10家，减少机构20家。总计减少机构10家

    # 目前这里将是对比昨天和今天的到达率,一些变量的名字将需要注意，这里并没有进行更改
    # 2018-03-14

    # listNeedNotSendDateWeek: add in -2018-04-02

    listBeforeYesterdayTotal = []
    tmpFileDir = "tmp"
    tmpFileName = "automatic_monitor.am"

    def __init__(self, fileUtilObj, dataTemplateObj, listNeedNotSendDateWeek):
        self.fileUtilObj = fileUtilObj
        self.dataTemplateObj = dataTemplateObj

        #if self.fileUtilObj.boolWhetherShowLog & True:
        #    self.fileUtilObj.writerContent(("今日listNeedNotSendDateWeek" + str(listNeedNotSendDateWeek)), 'runLog')

        self.listNeedNotSendDateWeek = listNeedNotSendDateWeek
        self.listBeforeYesterdayTotal = self.getListBeforeYesterdayTotal()
        if len(self.listBeforeYesterdayTotal) == 0:
            self.listBeforeYesterdayTotal = [{'shop_id': -1, 'org_id': -1}]
        else:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("缓存读取完成", 'runLog')


    def compareData(self, listYesterdayTotal):

        # dataTemplateObj: 数据存放模板
        # listYesterdayTotal： sql查询出的昨天的数据

        listBeforeYesterday = self.getValueForOrgAndShop(self.listBeforeYesterdayTotal)
        listYesterday = self.getValueForOrgAndShop(listYesterdayTotal)

        dictResult = self.compareListDataToGetIndex(listBeforeYesterday, listYesterday)
        dictNewResult = self.getDataByIndex(self.listBeforeYesterdayTotal, listYesterdayTotal, dictResult)
        self.showLogAndTemplate(dictNewResult)



    def getValueByKey(self, listTotal, strKey):

        # listTotal:是一个以dict为元素的list集合,这里例如self.listBeforeYesterdayTotal
        # strKey: 一个dict集合中存在的key，这里例如'org_id'等

        listResult = []
        for listTotalItem in listTotal:
            listResult.append(listTotalItem.get(strKey))

        return listResult

    def getValueForOrgAndShop(self, listTotal):

        # listTotal:是一个以dict为元素的list集合,这里例如self.listBeforeYesterdayTotal
        # 只获取右org_id和shop_id组合成的二维列表,0存放org_id的list，1存放shop_id的list
        # 因为list是有序的，所以这里的listOrgId和listShopId的值是对应的

        listOS = []
        listOrgId = self.getValueByKey(listTotal, 'org_id')
        listShopId = self.getValueByKey(listTotal, 'shop_id')

        listOS.append(listOrgId)
        listOS.append(listShopId)

        return listOS



    def compareListDataToGetIndex(self, listBeforeYesterday, listYesterday):

        # listBeforeYesterday: 二维list集合，0存放org_id的list，1存放shop_id的list
        # listYesterday: 和上一样，不过数据不同
        # 根据是否相同，取得下标
        # 返回的是下标

        dictResult = {}

        listBeforeYesterdayOrg = listBeforeYesterday[0]
        listBeforeYesterdayShop = listBeforeYesterday[1]

        listYesterdayOrg = listYesterday[0]
        listYesterdayShop = listYesterday[1]

        listTotalExistIndexForBY = []
        listTotalExistIndexForY = []

        listOnlyExistForBY = []
        listOnlyExistForY = []

        if (listBeforeYesterdayOrg[0] == -1 and
                listBeforeYesterdayShop[0] == -1):
            for indexY in range(len(listYesterdayOrg)):
                listOnlyExistForY.append(indexY)
        else:

            for indexBY in range(len(listBeforeYesterdayOrg)):
                for indexY in range(len(listYesterdayOrg)):

                    if(listBeforeYesterdayOrg[indexBY] == listYesterdayOrg[indexY] and
                            listBeforeYesterdayShop[indexBY] == listYesterdayShop[indexY]):
                        listTotalExistIndexForBY.append(indexBY)
                        listTotalExistIndexForY.append(indexY)

            for indexBY in range(len(listBeforeYesterdayOrg)):
                if indexBY not in listTotalExistIndexForBY:
                    listOnlyExistForBY.append(indexBY)

            for indexY in range(len(listYesterdayOrg)):
                if indexY not in listTotalExistIndexForY:
                    listOnlyExistForY.append(indexY)

        dictResult['listTotalExistIndexForBY'] = listTotalExistIndexForBY
        dictResult['listTotalExistIndexForY'] = listTotalExistIndexForY
        dictResult['listOnlyExistForBY'] = listOnlyExistForBY
        dictResult['listOnlyExistForY'] = listOnlyExistForY

        return dictResult


    def getDataByIndex(self, listBYtotal, listYtotal, dictResult):

        # listBYtotal: 前天的数据
        # listYtotal：昨天的数据
        # dictResult: 存放下标的dict集合，下标是从前面这两个参数的数据中得到的，存放的下标类型有三种
        # 一是前天的数据和昨天的数据中都有的，即共同数据key如：listTotalExistIndexForBY，listTotalExistIndexForY
        # 二是只有前天的数据中才有，key: listOnlyExistForBY
        # 三是只有昨天的数据中才有, key：listOnlyExistForY
        # 返回的是数据,而不是下标

        dictNewResult = {}
        listDataOnlyExistForBY = []
        listDataOnlyExistForY = []
        listTotalExist = []
        for indexBY in range(len(listBYtotal)):
            if indexBY in dictResult.get('listOnlyExistForBY'):
                listDataOnlyExistForBY.append(listBYtotal[indexBY])

        for indexY in range(len(listYtotal)):
            if indexY in dictResult.get('listOnlyExistForY'):
                listDataOnlyExistForY.append(listYtotal[indexY])
            else:
                listTotalExist.append(listYtotal[indexY])

        dictNewResult['listTotalExist'] = listTotalExist
        dictNewResult['listDataOnlyExistForBY'] = listDataOnlyExistForBY
        dictNewResult['listDataOnlyExistForY'] = listDataOnlyExistForY

        return dictNewResult

    def showLogAndTemplate(self, dictNewResult):

        # dictNewResult: 存放数据的dict

        # 添加新需求-->将减少的机构发送显示到dingTalk中
        # 添加判断，若增加或减少的机构为0，则日志中不打印
        # add --2018-03-28

        # 添加限定条件,即如限定周日周六两天不发送减少的机构列表到dingTalk中
        # add in -2018-04-02

        # 添加表格化输出,取消直接list打印
        # add in 2018-04-02

        listTotalExist = dictNewResult['listTotalExist']
        listDataOnlyExistForBY = dictNewResult['listDataOnlyExistForBY']
        listDataOnlyExistForY = dictNewResult['listDataOnlyExistForY']

        dictContentResult = self.judgeMentChangeForNew(listTotalExist, listDataOnlyExistForBY, listDataOnlyExistForY)
        strTotalReduceContent = ''

        prettyTableDo = PrettyTableDo()

        if len(listTotalExist) != 0:
            strTotalExistTable = prettyTableDo.getMsgForTableShowByListDict(listTotalExist, 1)
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent(((str(dictContentResult.get('strTotalExistContent'))) + "详情如下\n" + strTotalExistTable), 'runLog')
        # for listTotalExistItem in listTotalExist:
        #     self.fileUtilObj.writerContent(str(listTotalExistItem), 'runLog')

        if len(listDataOnlyExistForY) != 0:

            strDataOnlyExistForYTable = prettyTableDo.getMsgForTableShowByListDict(listDataOnlyExistForY, 1)

            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent(((str(dictContentResult.get('strOnlyAddContent'))) + "增加详情如下\n" + strDataOnlyExistForYTable), 'runLog')
            # for listDataOnlyExistForYItem in listDataOnlyExistForY:
            #     self.fileUtilObj.writerContent(str(listDataOnlyExistForYItem), 'runLog')
        else:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("无增加的机构", 'runLog')

        if len(listDataOnlyExistForBY) != 0:

            strDataOnlyExistForBYTable = prettyTableDo.getMsgForTableShowByListDict(listDataOnlyExistForBY, 1)

            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent(((str(dictContentResult.get('strOnlyReduceContent'))) + "减少详情如下\n" + strDataOnlyExistForBYTable), 'runLog')
            for listDataOnlyExistForBYItem in listDataOnlyExistForBY:
                # self.fileUtilObj.writerContent(str(listDataOnlyExistForBYItem), 'runLog')

                strTotalReduceContent += (listDataOnlyExistForBYItem.get('org_name') + " - " +
                                      listDataOnlyExistForBYItem.get('shop_name') + "\n\n")

        else:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("无减少的机构", 'runLog')

        if self.fileUtilObj.boolWhetherShowLog & True:
            self.fileUtilObj.writerContent((str(dictContentResult.get('strTotalChangeContent'))), 'runLog')

        self.dataTemplateObj.dataAll += ("[" + str(dictContentResult.get('strOnlyAddContent') +
                                                   dictContentResult.get('strOnlyReduceContent') +
                                                   dictContentResult.get('strTotalChangeContent')) + "]\n\n")

        strWeekNum = RunTime().getWeekNum()
        if strWeekNum in self.listNeedNotSendDateWeek:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent(("当前为周" + strWeekNum + ",不发送到钉钉"), 'runLog')
        else:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("今日减少机构列表信息将添加到消息模板中", 'runLog')
            if len(listDataOnlyExistForBY) != 0:
                self.dataTemplateObj.dataAll += "减少机构如下: \n\n" + strTotalReduceContent + "\n\n"


    def judgeMentChange(self, listTotalExist, listDataOnlyExistForBY, listDataOnlyExistForY):

        # listTotalExist
        # listDataOnlyExistForBY: 存放数据的list
        # listDataOnlyExistForY
        # 返回一个dict，内容为字符串

        dictContentResult = {}
        intTotalChange = (len(listDataOnlyExistForY) - len(listDataOnlyExistForBY))

        strTotalExistContent = ("昨天和前天都有签到的机构有 **" + str(len(listTotalExist)) + "** 家,")
        strOnlyAddContent = ("新增机构 **" + str(len(listDataOnlyExistForY)) + "** 家,")
        strOnlyReduceContent = ("减少机构 **" + str(len(listDataOnlyExistForBY)) + "** 家.")
        if intTotalChange > 0:
            strTotalChangeContent = ("总计增加机构 **" + str(intTotalChange) + "** 家.")
        elif intTotalChange < 0:
            listTotalChange = str(intTotalChange).split('-')
            strTotalChangeContent = ("总计减少机构 **" + str(listTotalChange[1]) + "** 家.")
        else:
            strTotalChangeContent = ("总计不变.")

        dictContentResult['strTotalExistContent'] = strTotalExistContent
        dictContentResult['strOnlyAddContent'] = strOnlyAddContent
        dictContentResult['strOnlyReduceContent'] = strOnlyReduceContent
        dictContentResult['strTotalChangeContent'] = strTotalChangeContent

        return dictContentResult



    def judgeMentChangeForNew(self, listTotalExist, listDataOnlyExistForBY, listDataOnlyExistForY):

        # listTotalExist
        # listDataOnlyExistForBY: 存放数据的list
        # listDataOnlyExistForY
        # 返回一个dict，内容为字符串

        # 添加对比昨天和今天的方法
        # 需求改变 --添加于2018-03-14

        dictContentResult = {}
        intTotalChange = (len(listDataOnlyExistForY) - len(listDataOnlyExistForBY))

        strTotalExistContent = ("昨天和今天都有签到的机构有 **" + str(len(listTotalExist)) + "** 家,")
        strOnlyAddContent = ("新增机构 **" + str(len(listDataOnlyExistForY)) + "** 家,")
        strOnlyReduceContent = ("减少机构 **" + str(len(listDataOnlyExistForBY)) + "** 家.")
        if intTotalChange > 0:
            strTotalChangeContent = ("总计增加机构 **" + str(intTotalChange) + "** 家.")
        elif intTotalChange < 0:
            listTotalChange = str(intTotalChange).split('-')
            strTotalChangeContent = ("总计减少机构 **" + str(listTotalChange[1]) + "** 家.")
        else:
            strTotalChangeContent = ("总计不变.")

        dictContentResult['strTotalExistContent'] = strTotalExistContent
        dictContentResult['strOnlyAddContent'] = strOnlyAddContent
        dictContentResult['strOnlyReduceContent'] = strOnlyReduceContent
        dictContentResult['strTotalChangeContent'] = strTotalChangeContent

        return dictContentResult



    def getListBeforeYesterdayTotal(self):

        # 从缓存文件中读取文件内容，并转换成list集合
        if self.fileUtilObj.boolWhetherShowLog & True:
            self.fileUtilObj.writerContent("准备从缓存文件中读取之前的数据...", 'runLog')

        listBYTotal = []

        intMark = self.fileUtilObj.checkFileExists(self.tmpFileDir + "/" + self.tmpFileName)
        if intMark == 1:
            strContent = self.fileUtilObj.readFileContent(self.tmpFileDir + "/" + self.tmpFileName)

            # 这里将读取到的缓存内容转换为list集合dict元素类型。因为缓存内容是一行内容，并不存在换行，所以可以转换
            # 如果修改缓存文件后,其内容存在多行,则在类型转换时会出错
            # 添加try-except异常处理--2018-03-29
            try:
                listBYTotal = eval(strContent)
            except:
                listBYTotal = [{'shop_id': -1, 'org_id': -1}]
                if self.fileUtilObj.boolWhetherShowLog & True:
                    self.fileUtilObj.writerContent("缓存内容转换list类型时出错,缓存内容如下", 'runLog')
                    self.fileUtilObj.writerContent(strContent, 'runLog')

        else:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("未发现缓存文件", 'runLog')
                listBYTotal = [{'shop_id': -1, 'org_id': -1}]

        strTableContent = PrettyTableDo().getMsgForTableShowByListDict(listBYTotal, 1)
        if self.fileUtilObj.boolWhetherShowLog & True:
            self.fileUtilObj.writerContent(("缓存中读取到的信息: " + strTableContent), 'runLog')

        return listBYTotal

    def writerListTotalToFile(self, listTotal):

        if self.fileUtilObj.boolWhetherShowLog & True:
            self.fileUtilObj.writerContent("准备将搜索得到的数据写入并覆盖缓存文件中的原有内容...", 'runLog')

        try:
            self.fileUtilObj.checkAndCreate(self.tmpFileDir)
            self.fileUtilObj.writerToFile(str(listTotal), self.tmpFileDir + "/" + self.tmpFileName, False)
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("写入缓存成功", 'runLog')
        except:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("数据写入缓存文件时出错", 'runLog')





