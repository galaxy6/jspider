#_*_coding=utf-8_*_


import scrapy
import multiprocessing
from common import md5
from common import get_netloc
from common import get_port 
from fetcher import UrlCollect
from filters import UrlFilter
from http import Capute
from scrapy.spiders import CrawlSpider,Rule
from jspider.items import TutorialItem
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from collections import defaultdict

class DemoSpider(CrawlSpider):
	
	name = 'jspider'
	rules =(
			Rule(LinkExtractor(allow=''),callback='parse_item',follow=True,process_links='filte',process_request='http_request'),
			)

	def __init__(self,url=None,*args,**kwargs):
		CrawlSpider.__init__(self,*args,**kwargs)
		self.url = url
		self.start_urls = ['%s'%url]
		self.allowed_domains = ['%s'%get_netloc(url)]
		self.urls_ = defaultdict(lambda:'none_value')
		self.asyn_capute()

	def parse_item(self,response):
		"""
		标签<a>数据提取
		标签<form>数据提取
		"""
		item = TutorialItem()
		item['link'] = UrlCollect(response.url,response).get_link()
		item['form'] = UrlCollect(response.url,response).post_form()
		#a/form数据提取
		return item
	

	def filte(self,links):
		"""
		去重功能的实现
		url量特别大的时候，使用列表时间复杂度增加，会越爬越慢；使用字典去重时间复杂度始终为一，不会有越爬慢的情况。
		"""
		links_ = []
		if links:
			for link in links:
				if link.url.find(get_netloc(self.url)):
					scheme = UrlFilter().get_scheme(link.url)
					if self.urls_[scheme] == "none_value":
						self.urls_.update({scheme:"1"})
						links_.append(link)
						
		return links_

	def http_request(self,request):
		"""
		过滤request
		"""
		return request

	def http_capute(self):
		"""
		嗅探当前http流量
		"""
		port = get_port(self.url)
		domain = get_netloc(self.url)
		cp = Capute(domain,port)

	def asyn_capute(self):
		"""
		使用多进程开启sniff模式，非多进程将会阻塞
		"""
		p = multiprocessing.Process(target=self.http_capute)
		p.start()
		
