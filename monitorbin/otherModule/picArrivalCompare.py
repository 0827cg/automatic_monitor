# -*- coding: utf-8 -*-

# author: cg错过
# time: 2018-01-11

import decimal

class PicArrivalCompare:

    # 前一天和昨天的图片到达率中获取对比设备的签到次数
    # 例如昨天和前天对比后得到：新增机构10家，减少机构20家。总计减少机构10家

    # 目前这里将是对比昨天和今天的到达率,一些变量的名字将需要注意，这里并没有进行更改
    # 2018-03-14

    listBeforeYesterdayTotal = []
    tmpFileDir = "tmp"
    tmpFileName = "automatic_monitor.am"

    def __init__(self, fileUtilObj, dataTemplateObj):
        self.fileUtilObj = fileUtilObj
        self.dataTemplateObj = dataTemplateObj
        self.listBeforeYesterdayTotal = self.getListBeforeYesterdayTotal()
        if len(self.listBeforeYesterdayTotal) == 0:
            self.listBeforeYesterdayTotal = [{'shop_id': -1, 'org_id': -1}]


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

        listTotalExist = dictNewResult['listTotalExist']
        listDataOnlyExistForBY = dictNewResult['listDataOnlyExistForBY']
        listDataOnlyExistForY = dictNewResult['listDataOnlyExistForY']

        dictContentResult = self.judgeMentChange(listTotalExist, listDataOnlyExistForBY, listDataOnlyExistForY)

        if self.fileUtilObj.boolWhetherShowLog & True:
            self.fileUtilObj.writerContent(((str(dictContentResult.get('strTotalExistContent'))) + "详情如下"), 'runLog')
        for listTotalExistItem in listTotalExist:
            self.fileUtilObj.writerContent(str(listTotalExistItem), 'runLog')

        if self.fileUtilObj.boolWhetherShowLog & True:
            self.fileUtilObj.writerContent(((str(dictContentResult.get('strOnlyAddContent'))) + "增加详情如下"), 'runLog')
        for listDataOnlyExistForYItem in listDataOnlyExistForY:
            self.fileUtilObj.writerContent(str(listDataOnlyExistForYItem), 'runLog')

        if self.fileUtilObj.boolWhetherShowLog & True:
            self.fileUtilObj.writerContent(((str(dictContentResult.get('strOnlyReduceContent'))) + "减少详情如下"), 'runLog')
        for listDataOnlyExistForBYItem in listDataOnlyExistForBY:
            self.fileUtilObj.writerContent(str(listDataOnlyExistForBYItem), 'runLog')

        if self.fileUtilObj.boolWhetherShowLog & True:
            self.fileUtilObj.writerContent((str(dictContentResult.get('strTotalChangeContent'))), 'runLog')

        self.dataTemplateObj.dataAll += ("[" + str(dictContentResult.get('strOnlyAddContent') +
                                                   dictContentResult.get('strOnlyReduceContent') +
                                                   dictContentResult.get('strTotalChangeContent')) + "]\n\n")


    def judgeMentChange(self, listTotalExist, listDataOnlyExistForBY, listDataOnlyExistForY):

        #listTotalExist
        # listDataOnlyExistForBY: 存放数据的list
        #listDataOnlyExistForY
        #返回一个dict，内容为字符串

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

        #listTotalExist
        # listDataOnlyExistForBY: 存放数据的list
        #listDataOnlyExistForY
        #返回一个dict，内容为字符串

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

        #从缓存文件中读取文件内容，并转换成list集合
        if self.fileUtilObj.boolWhetherShowLog & True:
            self.fileUtilObj.writerContent("准备从缓存文件中读取之前的数据...", 'runLog')

        listBYTotal = []

        intMark = self.fileUtilObj.checkFileExists(self.tmpFileDir + "/" + self.tmpFileName)
        if intMark == 1:
            strContent = self.fileUtilObj.readFileContent(self.tmpFileDir + "/" + self.tmpFileName)
            listBYTotal = eval(strContent)

        else:
            if self.fileUtilObj.boolWhetherShowLog & True:
                self.fileUtilObj.writerContent("未发现缓存文件", 'runLog')
                listBYTotal = [{'shop_id': -1, 'org_id': -1}]
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





