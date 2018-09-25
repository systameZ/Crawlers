# -*- coding: utf-8 -*-
import scrapy
import json
import re
from  weixin_moment.items import WeixinMomentItem
from weixin_moment.analyse import analyse_words
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
#https://chushu.la/book/chushula-554751434
class MomentSpider(scrapy.Spider):
    name = 'moment'
    allowed_domains = ['chushu.la']
    #start_urls = ['http://chushu.la/']
    start_urls=['https://chushu.la/api/book/chushula-554751434?isAjax=1']
    bookid='554751434'#224032223
    dict_w=[]

    def __init__(self):
        dispatcher.connect(self.spider_stopped, signals.engine_stopped)  ##建立信号和槽，在爬虫结束时调用
        dispatcher.connect(self.spider_closed, signals.spider_closed)  ##建立信号和槽，在爬虫关闭时调用

    def spider_closed(self):
        jsObj = json.dumps(self.dict_w)
        with open('moment.json', 'w') as fb:
            fb.write(jsObj)
        pass


    def spider_stopped(self):
        analyse_words()

    def start_requests(self):
        url = 'https://chushu.la/api/book/chushula-{0}?isAjax=1'.format(self.bookid)  # 获取目录的url
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        json_body = json.loads(response.body.decode('utf-8'))  # 加载json数据包
        catalogs = json_body['book']['catalogs']  # 获取json中的目录数据包
        url = 'https://chushu.la/api/book/wx/chushula-{0}/pages?isAjax=1'.format(self.bookid)  # 分页数据url
        start_page = 3  #int(catalogs[3]['month'])  # 获取起始月份作为index传值
        for catalog in catalogs:
            year = catalog['year']
            month = catalog['month']
            formdata = {
                "type": 'year_month',
                "year": year,
                "month": month,
                "index": str(start_page),
                "value": 'v_{0}{1}'.format(year, month)
            }
            start_page += 1
            yield scrapy.Request(
            url,
            method='POST',
            body=json.dumps(formdata),
            headers={'Content-Type': 'application/json'},
            callback=self.parse_moment)

    def parse_moment(self, response):
            """
            朋友圈数据处理
            """
            json_body = json.loads(response.body.decode('utf-8'))
            pages = json_body['pages']
            pattern = re.compile(u"[\u4e00-\u9fa5]+")  # 匹配中文
            item = WeixinMomentItem()
            for page in pages:
                if (page['type'] == "weixin_moment_page"):  # 仅抓取朋友圈分页数据
                    paras = page['data']['paras']
                    if paras:
                        moment = ''
                        for content in paras[0]['rows']:
                            result = re.findall(pattern,
                                                content['data'])  # 使用正则匹配所有中文朋友圈
                            moment += ''.join(result)
                        self.dict_w.append({"date":page['data']['dateText'],"moment":moment})
                        item["date"]=page['data']['dateText']
                        item["moment"] = moment
                        yield item
