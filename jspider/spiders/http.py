#_*_coding=utf-8_*_ 
import sys
import urlparse
import scapy_http.http as HTTP
from scapy.all import *
from scapy.error import Scapy_Exception
from filters import UrlFilter
from collections import defaultdict
from collections import deque
from common import md5
from jspider.pipelines import DemoPipeline

class Capute(object):
	'''
	嗅探数据包
	'''
	def __init__(self,host,port):
		self.host = host
		self.port = port
		self.static_ext = ['gif','css','jpg','png','.js']
		self.urls_ = defaultdict(lambda:'none_value')
		self.links_ = []
		self.pipeline = DemoPipeline()
		self.table_name = host.replace('.','_')
		self.run()	
				
	def pktTCP(self,pkt):
		if HTTP.HTTPRequest in pkt:
			test=pkt[TCP].payload
			if HTTP.HTTPRequest in pkt:
				if test.Method == "POST":
					headers,body= str(test).split("\r\n\r\n",1)
					path = "{0}?".format(test.Path) if test.Path[-1:] != "?" else test.Path
					link = "http://{0}{1}{2}".format(test.Host,path,body)
					if test.Host == self.host:
						scheme = UrlFilter().get_scheme(link)
						if self.urls_[scheme] == 'none_value':
							self.urls_.update({scheme:"1"})
							self.pipeline.insert_url(self.table_name,link,'POST',scheme,body)
				elif (test.Method == "GET"):					
					link = "http://{0}{1}".format(test.Host,test.Path)
					path = urlparse.urlparse(link).path
					if path[-3:] not in self.static_ext and test.Host == self.host:
						scheme = UrlFilter().get_scheme(link)
						if self.urls_[scheme] == "none_value":
							self.urls_.update({scheme:"1"})
							self.pipeline.insert_url(self.table_name,link,'GET',scheme,'')
				else:
					pass
	
	def run(self):
		sniff(filter='tcp and port {port}'.format(port=self.port),prn=self.pktTCP)


