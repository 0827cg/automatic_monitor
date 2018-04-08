#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# author: cg错过
# time  : 2018-04-02

from prettytable import PrettyTable

class PrettyTableDo:

    def getMsgForTableShowByListDict(self, listDictMsg, intPaddingLength):

        # listDictMsg: list集合数据,其元素未dict类型
        # 其内容例如:
        '''
        [{'org_name': '助成教育', 'rate': 100.0, 'org_id': 1941, 'shop_name': '助成教育思明分校', 'shop_id': 1290},
        {'org_name': '漳州伯乐教育', 'rate': 100.0, 'org_id': 2047, 'shop_name': '漳州伯乐教育', 'shop_id': 1398}]
        '''
        # 返回一个已经表格话的字符串类型数据

        listTableTitle = list(listDictMsg[0].keys())
        # strAlignTitle = listTableTitle[0]

        prettyTableContent = PrettyTable(listTableTitle)
        prettyTableContent.padding_width = intPaddingLength

        for listDictMsgItem in listDictMsg:

            listTableRowValue = []

            for listTitleItem in listTableTitle:
                listTableRowValue.append(listDictMsgItem[listTitleItem])

            prettyTableContent.add_row(listTableRowValue)

        return str(prettyTableContent)