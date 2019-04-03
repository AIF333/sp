# -*- coding: utf-8 -*-
import json
import time
from urllib.parse import urlencode

import scrapy
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from sp01.items import Sp01Item



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



## 测试爬虫 持久化抽屉网数据到文件

# class ChoutiSpider(scrapy.Spider):
#
#     name = 'chouti'
#     allowed_domains = ['chouti.com']
#     start_urls = ['https://dig.chouti.com/']
#
#     def parse(self, response):
#         hxs=HtmlXPathSelector(response)
#         item_list = hxs.select('//div[@id="content-list"]/div[@class="item"]')
#         # print('111',item_list)
#         for item in item_list:
#             # /:子标签  //:后代中找   .//当前位置后找    text():取文本  @属性:获取属性值
#             # extract:对象转为字符串列表    extract_first:对象转为字符串列表并取第一个元素
#             title=item.select('.//div[@class="part1"]/a/text()').extract()[0].strip()
#             url=item.select('.//div[@class="part1"]/a/@href').extract_first()
#
#             yield Sp01Item(title=title,url=url)
#
#             '''
#             持久化步骤：
#                 1.配置settings:
#                     # 持久化操作，后面的值建议 300-1000 之间会从小到大执行
#                     ITEM_PIPELINES = {
#                        'sp01.pipelines.Sp01Pipeline': 300,
#                        'sp01.pipelines.Sp02Pipeline': 301,
#                     }
#                 2.在回调函数（parse)中yield一个Item对象
#                 3.定义Item对象，在items.py中:
#                     class Sp01Item(scrapy.Item):
#                         # define the fields for your item here like:
#                         # name = scrapy.Field()
#                         title = scrapy.Field()
#                         url = scrapy.Field()
#                 4.编写pipelines.py
#                     这里最多可以定义5个方法：from_crawler(classmethod) , __init__ ,open_spider, process_item,close_spider
#                     调用顺序是：类方法  实例化方法  open_spider  process_item(多次) close_spider
#
#                      process_item中一般都会 return item 将item传递给后续的process_item方法，类似django中间件。如果不传递可以
#                      raise DronItem()
#
#                     （
#                         from scrapy.exceptions import DropItem
#                         raise DropItem()
#                     ）
#
#
#     # # 持久化  不推荐此操作，会不断打开关闭文件
#     # with open('xxx.log','a+',encoding='utf-8') as f:
#     #     f.write(title+"\n"+url+"\n")
#             '''


# 递归翻页爬取抽屉网数据
# class ChoutiSpider(scrapy.Spider):
#     name = 'chouti'
#     allowed_domains = ['chouti.com']
#     start_urls = ['https://dig.chouti.com/']
#
#     def parse(self, response):
#         hxs = HtmlXPathSelector(response)
#         item_list = hxs.select('//div[@id="content-list"]/div[@class="item"]')
#
#         # 获取文章列表中的标题和url
#         for item in item_list:
#             title = item.select('.//div[@class="part1"]/a/text()').extract()[0].strip()
#             url = item.select('.//div[@class="part1"]/a/@href').extract_first()
#
#             yield Sp01Item(title=title, url=url)
#
#
#         # 翻页
#         # re:test表明使用正则表达式
#         page_list = hxs.select('//div[@id="dig_lcpage"]//a[re:test(@href, "/all/hot/recent/\d+")]/@href').extract()
#         # page_list2 = hxs.select('//div[@id="dig_lcpage"]//a/@href').extract()
#         base_url="https://dig.chouti.com{0}"
#         # print(page_list)
#         for page in page_list:
#             # /all/hot/recent/2
#             # https: // dig.chouti.com / all / hot / recent / 3
#             url=base_url.format(page)
#             # print(url)
#             # 递归翻页  同最上面讲起始url start_urls 的爬虫类定义 方式一 方式二
#             # yield Item 会把数据给到 pipelines ; yield Request会把数据给到调度器
#             # # 翻页的层数  DEPTH_LIMIT=2 可在settings里进行设置
#             yield Request(url=url,callback=self.parse)


# 自动登录抽屉网并点赞
# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from scrapy.http.cookies import CookieJar
from scrapy import FormRequest


class ChoutiSpider(scrapy.Spider):
    # 爬虫应用的名称，通过此名称启动爬虫命令
    name = "chouti"
    # 允许的域名
    allowed_domains = ["chouti.com"]

    cookie_dict = {}
    has_request_set = {}

    # 起始url
    def start_requests(self):
        url = 'http://dig.chouti.com/'
        # return [Request(url=url, callback=self.login)]
        yield Request(url=url, callback=self.login)

    # 获取未认证的cookies，并进行登录
    def login(self, response):
        cookie_jar = CookieJar()
        cookie_jar.extract_cookies(response, response.request)

        # 登录获取未认证的cookie
        for k, v in cookie_jar._cookies.items():
            # print("====",v.items())
            for i, j in v.items():
                for m, n in j.items():
                    self.cookie_dict[m] = n.value
                    # print("---",j.items())

        data={
                "phone": "8613476152416",
                "password":"yt123456",
                "oneMonth": 1,
        }
        # 将字典转为url形式   phone=8613476152416&password=yt123456&oneMonth=1
        # print("--",urlencode(data))
        req = Request(
            url='https://dig.chouti.com/login',
            method='POST',
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
            body=urlencode(data)  ,
            cookies=self.cookie_dict,
            callback=self.check_login
        )
        yield req

    # 以登录身份进行首页访问  response是一个json.dumps字符串,可以转为对应格式
    def check_login(self, response):
        check_dict= json.loads(response.text)
        print("--check_dict--",check_dict,type(check_dict))
        if check_dict["result"]["code"] != '9999':
            print("登录失败,code!=9999")
            raise Exception("登录失败,code!=9999")
            return "登录失败,code!=9999"
        else:
            print("登录成功访问首页....")
            req = Request(
                url='http://dig.chouti.com/',
                method='GET',
                callback=self.show,
                cookies=self.cookie_dict,
                dont_filter=True ,  # 不参与剔重，这样就会再次访问，否则会直接忽视这个url，第一次已经访问了
            )
            yield req

    #
    def show(self, response):
        # print(response)
        # 找到文章的linksID进行点赞
        # 感觉 hxs.select() 和 hxs.xpath 一样呢，在解释时会用 xpath代替select
        hxs = HtmlXPathSelector(response)
        news_list = hxs.xpath('//div[@id="content-list"]/div[@class="item"]')
        for new in news_list:
            # temp = new.xpath('div/div[@class="part2"]/@share-linkid').extract()
            link_id = new.xpath('*/div[@class="part2"]/@share-linkid').extract_first()
            print("---",'http://dig.chouti.com/link/vote?linksId=%s' %(link_id,))
            yield Request(
                url='https://dig.chouti.com/link/vote?linksId=%s' %(link_id,),
                method='POST',
                cookies=self.cookie_dict,
                callback=self.do_favor
            )

        # 翻页
        page_list = hxs.select('//div[@id="dig_lcpage"]//a[re:test(@href, "/all/hot/recent/\d+")]/@href').extract()
        for page in page_list:

            page_url = 'http://dig.chouti.com%s' % page
            # 自定义过滤规则，即访问过的url就不再访问
            import hashlib
            hash = hashlib.md5()
            hash.update(bytes(page_url,encoding='utf-8'))
            key = hash.hexdigest()
            if key in self.has_request_set:
                pass
            else:
                self.has_request_set[key] = page_url
                yield Request(
                    url=page_url,
                    method='GET',
                    callback=self.show
                )
                time.sleep(3)

    def do_favor(self, response):
        print('11111',response.text)