#!/usr/bin/python3
#coding=utf-8

from monitorbin.operate import Operate

#author: cg错过
#time: 2017-10-10

def main():

    #linux系统服务器监控脚本
    #实现的监控服务有:
    #tomcat
    #nginx
    #redis
    #监控的项目服务模块化，每个项目中都设定了分两部分执行
    #一是每小时执行系统全检，只是检查不执行项目操作，全检后将发送邮件通知
    #二是依据定时器设置的时间来执行脚本检测项目，并提供项目操作。在当脚本检测到项目问题
    #后将执行操作一次，执行后若问题还在，则发送邮件通知
    #配置文件在于本文件同级目录的conf文件夹中
    

    operate = Operate()


if __name__ == '__main__':
    main()
