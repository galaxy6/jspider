#Jspider

##jspider

利用scrapy框架写的动态的爬取url的爬虫。

##Introduce
1.系统环境kail，脚本环境python2.x

2.重写scrapy的下载器，爬取的过程中直接模拟浏览器爬取网站的一般链接，form提交的post数据，js形成的数据，js点击形成的链接，ajax形成的链接。抓取经过本地网卡请求的本域名下的链接。

3.利用scapy抓取经过网卡的请求。


##Installation
In Kail, you need to install some libraries.

scrapy

splinter

phantomjs

MySQLdb

multiprocessing

scapy

scapy_http



mysql数据库配置

在./jspider/jspider/mysql.py文件的__init__初始函数中配置相关数据库参数。

	self.db_host = "localhost"  #数据库ip
	self.db_port = 3306         #数据库端口
	self.db_user = "root"       #数据库用户
	self.db_password= "xxxxx"   #数据库密码
	self.db_name = "xxxxx"      #数据库名字


##Usage
\#scrapy crawl jspider -a url=[URL]

例子
\#scrapy crawl jspider -a url=http://demo.aisec.cn/demo/aisec/ 

爬虫对demo.aisec.cn爬虫模拟战的链接抓取显示结果。

        [*] Starting at 18:07:09
        [INFO] [URL] http://demo.aisec.cn/robots.txt [GET] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/ [GET] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/ajax_link.php?id=1&t=0.5892525895033032? [DATA] [POST] 
        [INFO] [URL] http://demo.aisec.cn/ [GET] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/cookie_link.php?id=1 [GET] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/other/ [GET] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/login.php [GET] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/login2.php [GET] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/js_link.php?id=2&msg=abc [GET] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/html_link.php?id=2 [GET] 
        [INFO] [URL] http://demo.aisec.cn/files/wvs-testphp.png [GET] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/login.php [DATA]username=&password=123456 [POST] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/index.php [GET] 
        [INFO] [URL] http://demo.aisec.cn [GET] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/post_link.php [DATA]id=1&msg=abc&B1=提交 [POST] 
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/js_link.php?abc= [GET]
        [INFO] [URL] http://demo.aisec.cn/demo/aisec/click_link.php?id=2 [GET] 
        [*] shutting down at 18:07:26

数据库中链接的存储查询结果

        mysql> select id,url,body from demo_aisec_cn;

        +----+--------------------------------------------------------------------------+---------------------------+
        | id | url                                                                      | body                      |
        +----+--------------------------------------------------------------------------+---------------------------+
        |  1 | http://demo.aisec.cn/robots.txt                                          | NULL                      |
        |  2 | http://demo.aisec.cn/demo/aisec/                                         | NULL                      |
        |  3 | http://demo.aisec.cn/demo/aisec/ajax_link.php?id=1&t=0.5892525895033032? |                           |
        |  4 | http://demo.aisec.cn/                                                    | NULL                      |
        |  5 | http://demo.aisec.cn/demo/aisec/cookie_link.php?id=1                     | NULL                      |
        |  6 | http://demo.aisec.cn/demo/aisec/other/                                   | NULL                      |
        |  7 | http://demo.aisec.cn/demo/aisec/login.php                                | NULL                      |
        |  8 | http://demo.aisec.cn/demo/aisec/login2.php                               | NULL                      |
        |  9 | http://demo.aisec.cn/demo/aisec/js_link.php?id=2&msg=abc                 | NULL                      |
        | 10 | http://demo.aisec.cn/demo/aisec/html_link.php?id=2                       | NULL                      |
        | 11 | http://demo.aisec.cn/files/wvs-testphp.png                               | NULL                      |
        | 12 | http://demo.aisec.cn/demo/aisec/login.php                                | username=&password=123456 |
        | 13 | http://demo.aisec.cn/demo/aisec/index.php                                | NULL                      |
        | 14 | http://demo.aisec.cn                                                     | NULL                      |
        | 15 | http://demo.aisec.cn/demo/aisec/post_link.php                            | id=1&msg=abc&B1=提交      |
        | 16 | http://demo.aisec.cn/demo/aisec/js_link.php?abc=                         | NULL                      |
        | 17 | http://demo.aisec.cn/demo/aisec/click_link.php?id=2                      | NULL                      |
        +----+--------------------------------------------------------------------------+---------------------------+


补充：
由于是模拟浏览器的抓取的原因，抓取的过程相对于静态抓取时间会比较长。
为了增加爬虫的速度，我在downloadwebkit.py中注释掉了
\#self.click(browser,"a")
\#self.click(browser,"input")代码
即获取点击形成的url链接功能，如果为了抓取的更全面，可以去掉注释，但是耗费的时间较长。
