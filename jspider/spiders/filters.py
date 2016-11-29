#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re
import urlparse
from collections import deque
from common import md5

class UrlFilter(object):
	
	def __init__(self):
		self.urls = deque()

	def get_path(self,url):
		'''
		对url中的数字/中文/长度打于16的目录路径去重
		'''
		path = urlparse.urlparse(url).path
		#p_word = re.compile(r"[\u4e00-\u9fa5]+") #获取的源码中的url汉字利用这一种方式提取
		p_word = re.compile(r"(%\w{2})+")         #爬虫编码中url中汉字使用这一个方式，url编码
		path = p_word.sub(r'$',path)
		p_len = re.compile(r"[\w]{16,100}")
		path = p_len.sub(r'$',path)
		p = re.compile(r'\d+')
		path = p.sub(r'*',path)
		return path
	
	def get_params(self,url):
		'''
		对url中的参数中含有数字/中文/长度大于16的进行去重
		'''
		param = urlparse.urlparse(url).query
		#p_word = re.compile(u"[\u4e00-\u9fa5]+")
		p_word = re.compile(r"(%\w{2})+")
		param = p_word.sub(r'$',param)
		
		#处理参数的长度
		lens =  len(param[param.rfind('='):])	
		if lens >16:
			param = "%s=+" % param[:param.rfind('=')]
		p_len = re.compile(r'=.{16,100}&')
		param = p_len.sub(r'=+&', param)
		p = re.compile(r'\d+')
		param = p.sub(r'*',param)
		return param
	
	def get_scheme(self,url):
		'''
		获取去重模式
		'''
		scheme = "%s%s"%(self.get_path(url),self.get_params(url))
		scheme = md5(scheme)
		return scheme	
	
	def filter_url(self,scheme):
		'''
		去重的方法
		'''
		pass	
