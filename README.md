### automatic_monitor

#### 描述

一个监控linux服务器的python脚本


#### 功能

1. 实现的监控服务有:
    * tomcat
    * nginx
    * redis
	
2. 监控后将邮件提醒

监控的项目服务模块化，每个项目中都设定了分两部分执行，其中一是每小时执行系统全检，只是检查不执行项目操作，全检后将发送邮件通知；二是依据定时器设置的时间来执行脚本检测项目，并提供项目操作。在当脚本检测到项
目问题后将执行操作一次，执行后若问题还在，则发送邮件通知
配置文件在于本文件同级目录的conf文件夹中

#### 目前的配置项有

* [ProjectConfigure]
	* tomcatpath: tomcat安装文件的跟目录，例如有两个tomcat安装文件分别tomcat8080和tomcat8081。tomcat8080全路径为/home/dev/tomcat/tomcat8080，tomcat8081全路径为/home/dev/tomcat/tomcat8081。则此处填写/home/dev/tomcat
	* nginxpath: nginx安装路径
	* redispath: redis安装路径
	
* [UseConfigure]
	* servername: 填写服务器的别名，以此来辨别是哪台服务器
	* username: 此处填写的将用来作为邮件发送方的别称

* [LogConfigure]
	* logpath: 存放日志文件的文件夹路径

* [EmailConfigure]
	* smtp_server: smtp服务器地址，如 smtp.qq.com
	* email_sendaddr: 对应smtp的用来发送邮件的邮件地址账户
	* email_sendpasswd: 登陆smtp服务的授权码
	
* [ToEmail]
	*在此项下填写需要接受邮件的地址
	
* [RunConfigure]
	* run_intervals: 定时器间隔时间，表示脚本间隔多少秒检测一次，单位为秒
	* remove_log_time: 每天开始删除日志的时间点，清除时间太久远的日志，日志包括tomcat日志，nginx切割日志，自身日志(后期会添加删除多久以后的日志)，这里格式24小时制，比如: 23:50
	* showdebuglog: 是否将脚本打印的日志存放到日志文件中，默认是不存放到日志文件中，值：yes/no
	
	
第一次运行或者没有配置文件，脚本将会自动初始化配置文件


注: 个人项目，不定期维护更新


author: cg错过

createTime: 2017-09-30

firstCommitTime: 2017-11-01