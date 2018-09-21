### automatic_monitor

#### 描述

一个监控linux服务器的python脚本,使用python3.5


#### 功能

1. 实现的监控服务有:
    * tomcat
    * nginx
    * redis
    * 磁盘
    * 数据库某个字段的变化(只是现在接触的项目需求，索性就作为模块加在这个工具中)
    * pm2

以上的服务如若有不需要检测的，可以在配置文件中进行注释该项，即可不被检测.就如检测数据库某个字段的变化，这个功能一直觉得不适合放到这里，所以在配置文件中添加了一项配置，是否启用去检测该项。下面会有说明
后期该是会打算将这个模块删除
关于数据库字段和图片到达率这两块，后期将删除

	
2. 监控后消息提醒方式现在有两种:
    * email邮件提醒
    * dingTalk钉钉机器人提醒

可以选择使用那种方式来提醒

监控的项目服务模块化，每个项目中都设定了分两部分执行, ~~其中一是每小时执行系统全检~~,其中一是每天执行服务全检,只是检查不执行项目操作，全检后将发送邮件通知；二是依据定时器设置的时间来执行脚本检测项目，并提供项目操作。在当脚本检测到项
目问题后将执行操作一次，执行后若问题还在，则发送邮件通知
配置文件在于本文件同级目录的conf文件夹中

#### 目前的配置项有

* [ProjectConfigure]
	* tomcatpath: tomcat安装文件的跟目录，例如有两个tomcat安装文件分别tomcat8080和tomcat8081。tomcat8080全路径为/home/dev/tomcat/tomcat8080，tomcat8081全路径为/home/dev/tomcat/tomcat8081。则此处填写/home/dev/tomcat
	* nginxpath: nginx安装路径
	* redispath: redis安装路径

* [Pm2]
    * whether_check_pm2 : 是否检测pm2,yes/no
	* pro_for_letter: 检测pm2搭载的项目名,将监控这个运行的项目是否运行正常,执行重启操作
	
* [UseConfigure]
	* servername: 填写服务器的别名，以此来辨别是哪台服务器
	* username: 此处填写的将用来作为邮件发送方的别称

* [LogConfigure]
	* logpath: 存放日志文件的文件夹路径
	* whether_rm_log: 是否执行删除日志操作
	* rm_log_passday: 删除多少天前的日志
	* when_time_rm: 在一天中的那个时候开始执行删除日志操作,单位：hour

* [EmailConfigure]
    * email: 值为yes/no，是否使用email来发送结果消息
	* smtp_server: smtp服务器地址，如 smtp.qq.com
	* email_sendaddr: 对应smtp的用来发送邮件的邮件地址账户
	* email_sendpasswd: 登陆smtp服务的授权码
	
* [ToEmail]
	*在此项下填写需要接受邮件的地址

* [Dingtalk]
    * dingtalk: yes/no,是否使用dingTalk来发送结果消息
    * webhook: 钉钉机器人url

* [DiskConfigure]
    * checkdisk: yes/no,是否检测磁盘
    * warning_level: 报警标准,单位为%,当磁盘各节点中如有一个节点空间使用量超过了这个值，将按脚步执行频率来发送消息

* [CheckLetterConfigure]
    * whether_check_letter: yes/no,是否检测数据库某个字段
    * table_name: 表名字
    * field_name: 需要检测的字段名
    * fieldcompare_name1: 需要获取结果的字段1
    * fieldcompare_name2: 需要获取结果的字段2
    * fieldcompare_namevalue: 用来查询条件的字段名
    * first_field_value: 该字段的第一个值
    * next_field_value: 该字段的第二个变化的值
    * sleeptime: 查询数据时休眠时间,单位秒
    * past_days_num : 检测多少天前的，例如3天即3

* [MysqlConfigure]
    * host: 数据库服务器地址
    * port: 端口
    * user: 用户名
    * passwd: 密码
    * database: 库名字

* [Pic_Arrivals]
    * whether_check_pic: 是否检测图片到达率
    * sql_path: 存放该sql查询语句的的文件路径
	* arrivals_standard: 一个到达率的标准值，如果低于这个值将会进行记录
    * number_accuracy: 保留的小数点个数
	* need_not_send_dateweek: 规定在那些天(以具体周几来设置)将一些检测到的未使用设备的机构列表不发送到钉钉(消息通知)

	
* [RunConfigure]
	* run_intervals: 定时器间隔时间，表示脚本间隔多少秒检测一次，单位为秒
    * when_hour_checkall: 每天的哪个小时进行概括性的检测
	* remove_log_time: 每天开始删除日志的时间点，清除时间太久远的日志，日志包括tomcat日志，nginx切割日志，自身日志(后期会添加删除多久以后的日志)，这里格式24小时制，比如: 23:50
	* savelog_to_file: 是否将脚本打印的日志存放到日志文件中，默认是不存放到日志文件中，值：yes/no
    * time_beginning: ×
    * time_end: × time_beginning和time_end表示一个时间段，用来发送消息

#### 使用到的模块

* pymysql
* prettyTable

#### 运行实例

1. 如果没安装pymysql和prettyTable，需要先安装这个模块
    运行命令`pip3 install pymysql`及`pip3 install prettyTable`

2. 进入这个目录，使用命令`python3 monitor.py`即可运行,如果需要持续化运行,可以使用命令`nohup python3 monitor.py &`

	
第一次运行如果没有配置文件，脚本将会自动初始化配置文件

#### 不足

~~后期有空将实现数据的表格化，提高数据的可读性。虽然有个PrettyTable模块，但感觉并不全面，打算自己
写个模块~~

现在看那会儿写的代码, 太乱了(`add in 2018-09-21 11:56`)


> 注: 个人项目，不定期维护更新

> author: cg错过

> createTime: 2017-09-30

> firstCommitTime: 2017-11-01
