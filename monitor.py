#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from monitorbin.operate import Operate

# author: cg
# time: 2017-10-10

def main():

    # linux系统服务器监控脚本
    # 实现的监控服务有:
    # tomcat
    # nginx
    # redis
    # 监控的项目服务模块化，每个项目中都设定了分两部分执行
    # 一是每小时执行系统全检，只是检查不执行项目操作，全检后将发送邮件通知
    # 二是依据定时器设置的时间来执行脚本检测项目，并提供项目操作。在当脚本检测到项目问题
    # 后将执行操作一次，执行后若问题还在，则发送邮件通知
    # 配置文件在于本文件同级目录的conf文件夹中
    

    operate = Operate()


if __name__ == '__main__':
    main()



'''
======================
### 发现的问题与计划

* 2018.02.05: 记入在/monitorbin/module/diskCheck.py中checkUse()方法中
* 2018.02.05: 日志打印元素为dict的list集合时，计划添加表格来格式化打印输出

* 2018.03.01: 添加重启pm2搭载的项目功能,主要是放在当检测有未推送消息时，来进行重启

* 2018-03-02:
* 有个bug，在/monitorbin/module/diskCheck.py文件下
* 代码: intMountPointsNum = int(intTotalNum) - 1
* 出错: ValueError: invalid literal for int() with base 10: ''
* 尝试修改成: intMountPointsNum = int(float(intTotalNum)) - 1

* 2018-03-26: 有个bug,在/monitorbin/module/diskCheck.py中的代码
* self.dataTempObj.dataAll += "> 超过的节点如下\n" + "> " + listOutMsg,
* 有两处没有进行对list的类型转换，转string类型.现已经添加类型转换str(listOutMsg)

======================
'''
