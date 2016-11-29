#-*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
import time
import signal
import datetime
from scrapy import signals
from mysql import db
from jspider.spiders.common import get_netloc
from jspider.spiders.filters import UrlFilter
from jspider.spiders.common import md5
from jspider.spiders.common import G,W

class DemoPipeline(object):

	def open_spider(self,spider):
		"""
		初始化url数据表
		"""
		print '[*] Starting at {time_}'.format(time_=datetime.datetime.now().strftime('%H:%M:%S'))
		db_name = db().db_name
		table_name = spider.allowed_domains[0].replace('.','_')
		count = db().query("select count(*) from information_schema.tables where table_schema = '{db_name}' and table_name = '{table_name}'".format(db_name=db_name,table_name=table_name))
		if count == (0L,):
			db().update("create table "+table_name+" (id int(10) NOT NULL primary key auto_increment,url varchar(400) NOT NULL,types char(4) NOT NULL,body varchar(1000),source varchar(20) not null default 'crawler',scheme varchar(100) not null,time varchar(30) not null)")
	
	def process_item(self, item, spider):
		"""
		对url数据入库分类处理
		"""
		host = spider.allowed_domains[0]
		table_name = host.replace('.','_')
		for url in item['link']:
			if(get_netloc(url) == host):
				scheme = UrlFilter().get_scheme(url)
				self.insert_url(table_name,url,'GET',scheme,'')
		for url_ in item['form']:
			if(get_netloc(url_) == host):
				urls_ = []
				urls_ = url_.split('?')
				scheme = UrlFilter().get_scheme(url_)
				self.insert_url(table_name,urls_[0],'POST',scheme,urls_[1])
		return item
	def close_spider(self,spider):
		"""
		关闭scapy的sniff功能
		"""
		print '[*] shutting down at {time_}'.format(time_=datetime.datetime.now().strftime('%H:%M:%S'))
		self.kill_process()

	def kill_process(self):
		"""
		杀死当前的进程和sniff进程
		"""
		own = os.getpid()
		result = os.popen('ps aux')
		res = result.read()
		for line in res.splitlines():
			if 'jspider' in line:
				pid = int(line.split(None,2)[1])
				if pid != own:
					os.kill(pid,signal.SIGKILL)
		os.kill(own,signal.SIGKILL)

	def insert_url(self,table_name,url,types,scheme,body):
		"""
		数据入库
		"""
		if types == "GET":
			result = db().query("select count(*) from {table_name} where scheme = '{scheme}'".format(table_name=table_name,scheme=scheme))
			if result == (0L,):
				print G+'[INFO] [URL] {url} [{types}] {W}'.format(types=types,url=url,W=W)
				db().update("insert into {table_name}(url,types,scheme,time) values('{url}','{types}','{scheme}','{time_}')".format(table_name=table_name,url=url,types=types,scheme=scheme,time_=time.time()))
		elif types == "POST":
			result = db().query("select count(*) from {table_name} where scheme = '{scheme}'".format(table_name=table_name,scheme=scheme))
			if result == (0L,):
				print G+'[INFO] [URL] {url} [DATA]{body} [{types}] {W}'.format(types=types,url=url,body=body,W=W)
				db().update("insert into {table_name}(url,types,body,scheme,time) values('{url}','{types}','{body}','{scheme}','{time_}')".format(table_name=table_name,url=url,types=types,body=body,scheme=scheme,time_=time.time()))
		else:
			print "[ERROR] Error in data storage!"
