# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class Sp01Pipeline(object):
    def open_spider(self, spider):
        """
        爬虫开始执行时，调用  如 打开数据库连接
        :param spider:
        :return:
        """
        self.f=open('xxxxx.log','w+',encoding='utf-8')
        print("开始")

    def process_item(self, item, spider):
        '''
         每yield一次执行一次
        '''
        self.f.write(item["title"]+"\n"+item["url"]+"\n")
        self.f.flush()
        return item # 传值给后续的 process_item
        # raise DropItem() 后续的process_item将不会再执行


    def close_spider(self, spider):
        """
        爬虫关闭时，被调用  如关闭数据库连接
        :param spider:
        :return:
        """
        self.f.close()
        print("结束")

class Sp02Pipeline(object):
    def process_item(self, item, spider):
        return item
