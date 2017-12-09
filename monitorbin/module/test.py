
def main():

    listMountPointsMsg = [{'type': 'xfs', 'size': '20G', 'filesystem': '/dev/vda1', 'mountedon': '/',
                           'use': '51%', 'used': '11G', 'avail': '9.9G'}, {'type': 'devtmpfs', 'size': '1.9G',
                                                                           'filesystem': 'devtmpfs', 'mountedon': '/dev',
                                                                           'use': '0%', 'used': '0', 'avail': '1.9G'}, {'type': 'tmpfs', 'size': '1.9G', 'filesystem': 'tmpfs', 'mountedon': '/dev/shm', 'use': '0%', 'used': '0', 'avail': '1.9G'}]
    listCutMountPointsMsg = formatMsgForSendAll(listMountPointsMsg)
    formatMsgForSendAllToStr(listCutMountPointsMsg)

def formatMsgForSendAll(listMountPointsMsg):

    listCutMountPointsMsgName = ['mounton', 'used', 'use']
    listCutMountPointsMsg = []
    listCutMountPointsMsg.append(listCutMountPointsMsgName)
    for dictMountPointsMsgItem in listMountPointsMsg:
        listCutMountPointsMsgValue = []
        listCutMountPointsMsgValue.append(dictMountPointsMsgItem.get('mountedon'))
        listCutMountPointsMsgValue.append(dictMountPointsMsgItem.get('used'))
        listCutMountPointsMsgValue.append(dictMountPointsMsgItem.get('use'))
        listCutMountPointsMsg.append(listCutMountPointsMsgValue)

    print(listCutMountPointsMsg)
    return listCutMountPointsMsg


def formatMsgForSendAllToStr(listCutMountPointsMsg):

    strMsgForSendAll = ""

    for listCutMountPointsMsgItem in listCutMountPointsMsg:
        strMsgForSendAll += "\t - "
        for index in range(3):
            strMsgForSendAllLine = listCutMountPointsMsgItem[index]
            strMsgForSendAll += strMsgForSendAllLine + "\t"
        strMsgForSendAll += "\n"

    print(strMsgForSendAll)


if __name__ == '__main__':
    main()
