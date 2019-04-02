# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector



# # 方式一
# class ChoutiSpider(scrapy.Spider):
#     '''
#     引擎ScrapyEngine将Spiders中的start_urls传入给调度Scheduler，Downloder从调度获取start_urls，完成连接网络下载后，
#     执行回调callback函数（未定义，则默认执行parse函数）
#     '''
#     name = 'chouti'
#     allowed_domains = ['chouti.com']
#     start_urls = ['https://dig.chouti.com/']
#
#     def parse(self, response):
#         print("下载完成",response)
# # 方式二
# class ChoutiSpider(scrapy.Spider):
#     '''
#     引擎ScrapyEngine将Spiders中的Request对象（包括起始url-start_url，和回调函数）传入给调度Schedule，Downloader从调度中获取
#     Request对象，先执行url连接网络，后执行定义的回调函数
#     '''
#     name = 'chouti'
#     allowed_domains = ['chouti.com']
#
#     def start_requests(self):
#         '''
#         需要返回一个可迭代对象，即源码内部会是  x=iter(x),然后next(x)来取值，列表也是可迭代对象，所以 yield生成器和列表是一样的，都可以作为返回
#         '''
#         # 返回方式一
#         yield Request(url='https://dig.chouti.com/',callback=self.parse11)
#         yield Request(url='https://baidu.com/',callback=self.parse22)
#
#         # 返回方式二
#         # return [
#         #     Request(url='https://dig.chouti.com/', callback=self.parse11),
#         #     Request(url='https://baidu.com/', callback=self.parse22),
#         # ]
#
#     def parse11(self, response):
#         print("下载完成11",response)
#
#     def parse22(self, response):
#         print("下载完成22",response)



# 测试爬虫
from sp01.items import Sp01Item


class ChoutiSpider(scrapy.Spider):

    name = 'chouti'
    allowed_domains = ['chouti.com']
    start_urls = ['https://dig.chouti.com/']

    def parse(self, response):
        hxs=HtmlXPathSelector(response)
        item_list = hxs.select('//div[@id="content-list"]/div[@class="item"]')
        # print('111',item_list)
        for item in item_list:
            # /:子标签  //:后代中找   .//当前位置后找    text():取文本  @属性:获取属性值
            # extract:对象转为字符串列表    extract_first:对象转为字符串列表并取第一个元素
            title=item.select('.//div[@class="part1"]/a/text()').extract()[0].strip()
            url=item.select('.//div[@class="part1"]/a/@href').extract_first()

            yield Sp01Item(title=title,url=url)

            '''
            持久化步骤：
                1.配置settings:
                    # 持久化操作，后面的值建议 300-1000 之间会从小到大执行
                    ITEM_PIPELINES = {
                       'sp01.pipelines.Sp01Pipeline': 300,
                       'sp01.pipelines.Sp02Pipeline': 301,
                    }
                2.在回调函数（parse)中yield一个Item对象
                3.定义Item对象，在items.py中:
                    class Sp01Item(scrapy.Item):
                        # define the fields for your item here like:
                        # name = scrapy.Field()
                        title = scrapy.Field()
                        url = scrapy.Field()
                4.编写pipelines.py
                    这里最多可以定义5个方法：from_crawler(classmethod) , __init__ ,open_spider, process_item,close_spider
                    调用顺序是：类方法  实例化方法  open_spider  process_item(多次) close_spider
                    
                     process_item中一般都会 return item 将item传递给后续的process_item方法，类似django中间件。如果不传递可以
                     raise DronItem()
                     
                    （   
                        from scrapy.exceptions import DropItem
                        raise DropItem()
                    ）
                    
                   
    # # 持久化  不推荐此操作，会不断打开关闭文件
    # with open('xxx.log','a+',encoding='utf-8') as f:
    #     f.write(title+"\n"+url+"\n")
            '''
