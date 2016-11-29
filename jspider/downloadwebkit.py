#_*_coding=utf-8_*_
from splinter import Browser
from scrapy.http import HtmlResponse

class Downloader(object):
	
	def process_request(self,request,spider):
		'''
		重写下载器,利用phantomjs请求url
		'''
		browser = Browser('phantomjs')
		browser.visit(request.url)
		#self.click(browser,"a")
		#self.click(browser,"input")
		response = browser.html
		browser.quit()
		response = str(response.encode('utf-8'))
		return HtmlResponse(request.url,body=response)

	def click(self,browser,tag):
		'''
		点击事件
		'''
		a_list = browser.find_by_xpath("//%s[@onclick]"%tag)
		while a_list:
			a_list.click()
			a_list.pop(0)
			if not a_list:
				break
		
