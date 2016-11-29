# _*_ coding: utf-8 _*_

import re
from common import md5
from filters import UrlFilter
from common import get_baseurl
from common import get_urlpath
from common import filter_keyword
from collections import deque
from collections import defaultdict

class UrlCollect(object):
    
    def __init__(self,url,response):
        """ 
        @param: url 当前url
        @param: response 当前url的源码
       	"""
       	self.url = url
       	self.response = response
        self.urls_ = defaultdict(lambda:'none_value')
        self.links_ = deque()

    def get_link(self):
        """
        获取a标签链接
        """
        links = self.response.xpath("//a/@href").extract()
        urls = self.url_list(links)
        return urls

    def url_list(self,links):
        """
        把提取的url链接整理成统一的格式
        参数links: url链接列表
        """

        urls = deque()
        base_url = get_baseurl(self.url)
        url_path = get_urlpath(self.url)
        pattern = re.compile("/")
        array  = pattern.findall(url_path)
        if len(array)>3:
            path = url_path[0:url_path.rfind('/',0,len(url_path))]
            path_ = path[0:path.rfind('/',0,len(path))]
        else:
            path=base_url
            path_=base_url

        for link in links:
            link = filter_keyword(link)
            if(link !="" and link != None and link != "None"):
                if(link[:1] == "/"):
                    link_ = "%s%s"%(base_url,link)
                elif(link[:7] == "http://" or link[:8] == "https://"):
                    link_ = "%s"%link
                elif(link[:2] == "//"):
                    link_ = "http://%s"%link 
                elif(link[:1] == "?"):
                    link_ = "%s%s"%(url_path,link)
                elif(link[:3] =="../"):
                    link = link[2:]
                    link_ = "%s%s"%(path_,link)
                elif(link[:2] =="./"):
                    link = link[1:]
                    link_ = "%s%s"%(path,link)
                else:
                    link_ = "%s/%s"%(path,link)
                urls.append(link_) if (link_ not in urls) else None
        return urls
    
    def form_url(self,action):
        """
        主要是处理form表单提取的url列表和参数
        """
        base_url = get_baseurl(self.url)
        url_path = get_urlpath(self.url)
        pattern = re.compile("/")
        array  = pattern.findall(url_path)
        if len(array)>3:
            path = url_path[0:url_path.rfind('/',0,len(url_path))]
            path_ = path[0:path.rfind('/',0,len(path))]
        else:
            path=base_url
            path_=base_url
        if(action != None and action !="" and action !="None"):          
            if(action[:1] == "/"):
                action_ = "%s%s" % (base_url,action)
            elif(action[:7] == "http://" or action[:8] == "https://"): 
                action_ = "%s" %action
            elif(action[:3] =="../"):
                action = action[2:]
                action_ = "%s%s" % (path_,action)
            elif(action[:2] =="./"):
                action = action[1:]
                action_ = "%s%s" % (path,action)
            elif(action[:1] == "#" or action[:1] == "?"):
                action_ = self.url
            else:
                action_ = "%s/%s" % (path,action)
        else:
            action_ = self.url
        return action_
	
    def post_form(self):
        """
       	获取表单的内容并写出特定的格式
		eg:
			url: http://www.xxx.com/save.jsp 
			data: id=1&action=submit
			==> http://www.xxx.com/save.jsp?id=1&action=submit
        """
        urls = deque()
        
        action_nodes = self.response.xpath("//form/@action").extract()
		
        if action_nodes.__len__ >0:
            nodes_len = action_nodes.__len__()
            for k in range(1, nodes_len+1):
                action_nodes_string = "//form[%s]/@action" % k
                if self.response.xpath(action_nodes_string).extract():
                    nodes_list = self.response.xpath(action_nodes_string).extract()
                    input_string = "//form[%s]//input[@name]/@name" % k
                    elements = self.response.xpath(input_string).extract()
                    elements_len = elements.__len__()
                    lists = []
                    params = ""
                    for i in range(1,elements_len+1):
                        string = "//form[%s]//input[@name][%s]/@value" % (k,i)
                        if self.response.xpath(string):
                            elements_value =  self.response.xpath(string).extract()
                            elements_value_string = ''.join(elements_value)
                            lists.append(elements_value_string)
                        else:
                            lists.append("123456")  
                    for index in range(elements_len):           
                        param = "%s=%s&" % (elements[index],lists[index])
                        params = params + param
                    params = params[:-1] if (params[-1:] == '&') else params
                    url_params = self.form_url(nodes_list[0])
                    url = "%s?%s"%(url_params,params)
                    if isinstance(url,unicode):
                        url = url.encode("utf-8")
                    urls.append(url) if (url not in urls) else None
            return urls
	
