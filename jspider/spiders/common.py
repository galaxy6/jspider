#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
import urlparse
import signal

G = '\033[92m' #green
Y = '\033[93m' #yellow
B = '\033[94m' #blue
R = '\033[91m' #red
W = '\033[0m'  #white
 
def get_netloc(link):
	"""
	获取域名
	"""
	netloc = urlparse.urlparse(link).netloc
	return netloc

def get_port(link):
	"""
	获取web服务器端口
	"""
	port = urlparse.urlparse(link).port
	port = port if port and port!="None" else '80'
	port_ = '{port}'.format(port=port) if port!=443 else '80'
	return port_
	
def get_baseurl(link):
    """
    这个函数的主要作用是得到url的访问协议和域名
    参数： url链接
    """
    netloc = urlparse.urlparse(link).netloc
    scheme = urlparse.urlparse(link).scheme
    url = "%s://%s" %(scheme,netloc)
    return url  


def get_urlpath(link):
    """
    这个函数的主要作用是得到url的协议域名路径
    参数： url链接
    """
    netloc = urlparse.urlparse(link).netloc
    scheme = urlparse.urlparse(link).scheme
    path = urlparse.urlparse(link).path
    url = "%s://%s%s" %(scheme,netloc,path)
    return url

def md5(string):
	"""
	md5加密算法
	"""
	import hashlib
	import types
	if type(string).__name__ == "unicode":
		string = string.encode("utf-8")
	if type(string) is types.StringType:
		m = hashlib.md5()
		m.update(string)
		return m.hexdigest()
	else:
		return "None"

def filter_keyword(url):
	"""
	1.过滤url中错误的url
	2.scrapy爬虫已有对静态url过滤机制，ext中的后缀不会过滤
	eg:
		ext = ['flv','apk','7z','bak','iso','tar','tar.gz','log','js']
	"""
	filter_keyword = ['javascript','tel:','mailto','logout']
	for _ in filter_keyword:
		if (_ in url):
			url = ""
	if(url[:1] == "#" or url[:1] =="?"):
		url = ""
	url = url.replace('&amp;','&')
	url = url.replace(' ','')
	url = url.strip()
	return url

