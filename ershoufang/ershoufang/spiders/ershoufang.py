# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import etree
from scrapy.spider import Spider
from scrapy.selector import Selector
from ..items import ErshoufangItem
import time
import datetime
import csv
class ErshoufangSpider(Spider):  
    name = 'ershoufang'    
    allowed_domains = ['lianjia.com']
    #二手房频道
    #start_urls = [    'http://bj.lianjia.com/ershoufang/' ]
    #东城
    #start_urls = [    'http://bj.lianjia.com/ershoufang/dongcheng/pg1/' ]
    #最新发布
    start_urls = [    'http://bj.lianjia.com/ershoufang/co32/' ]
    #海淀最新发布
    start_urls = [    'http://bj.lianjia.com/ershoufang/']
    
    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                         Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        yield scrapy.Request(url=self.start_urls[0], headers=headers, method='GET', callback=self.parse)

    #获取配置文件信息
    def get_cfg(self,cfg_type):
        cfgs=[]
        if cfg_type=='xiaoqu':
            #csv_reader = csv.reader(open('../../cfg/xiaoqu.csv'))
            csv_reader = csv.reader(open('./cfg/xiaoqu.csv'))
            i=0
            for row in csv_reader:
                i=i+1
                if i==1:
                    continue                    
                #1,上地学区,上地东里,1111046342806,1
                chn_name=row[2]
                xiaoqu_id=row[3]
                v=row[4]                
                if v=='1':
                    cfgs.append([chn_name,xiaoqu_id])
                    print chn_name,xiaoqu_id,v
        return cfgs
			
	
    #获取输入的urls列表,返回数组
    def get_input_urls(self,url_type):
        urls = []
        #分区域
        if url_type=='quyu':
            area_list = [ 'dongcheng','xicheng','haidian','chaoyang']
            for area in area_list:
                for j in range(1,5):
                    url = 'http://bj.lianjia.com/ershoufang/{}/pg{}co32/'.format(area,str(j))
                    urls.append(url)
        elif  url_type=='xiaoqu':
            #厂洼
            cfgs=self.get_cfg('xiaoqu')
            for cfg in cfgs:
                #http://bj.lianjia.com/xiaoqu/1111027379186/
                #url = 'http://bj.lianjia.com/xiaoqu/{}/'.format(cfg[1])
                #http://bj.lianjia.com/ershoufang/c1111027379186/
                url = 'http://bj.lianjia.com/xiaoqu/c{}/'.format(cfg[1])
                urls.append(url)
        return urls
    
    #开始对网页进行处理
    def parse(self, response):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                                 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        print u'-------------开始抓取页面-------------'
        #urls=self.get_input_urls('xiaoqu')
        urls=self.get_input_urls('quyu')
        print urls
        items=[]
        i=1            
        for url in urls:     
            print url
            p = requests.get(url)
            contents = etree.HTML(p.content.decode('utf-8'))
            houselist = contents.xpath('/html/body/div[4]/div[1]/ul/li')

            #每个新网页都暂停2秒
            time.sleep(0.1)
            for house in houselist:
                print i,
                i=i+1
                try:
                        title = house.xpath('div[1]/div[1]/a/text()').pop()
                        print title
                        item = ErshoufangItem()
                        item['title'] = house.xpath('div[1]/div[1]/a/text()').pop()
                        item['community'] = house.xpath('div[1]/div[2]/div/a/text()').pop()
                        item['model'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[1]
                        #print item['model']
                        item['area'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[2].decode('gb18030')
                        item['focus_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[0]
                        item['watch_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[1].decode('gb18030')
                        item['time'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[2]
                        item['price'] = house.xpath('div[1]/div[6]/div[1]/span/text()').pop()
                        item['average_price'] = house.xpath('div[1]/div[6]/div[2]/span/text()').pop()
                        item['link'] = house.xpath('div[1]/div[1]/a/@href').pop()
                        #http://bj.lianjia.com/ershoufang/101101161651.html
                        item['house_id'] =  house.xpath('div[1]/div[1]/a/@href').pop().split('/')[-1].split('.')[0]
                        #item['city'] = response.meta["id1"]
                        self.url_detail = house.xpath('div[1]/div[1]/a/@href').pop()
                        item['Latitude'] = '-1,-1'#self.get_latitude(self.url_detail)                        
                        #print item
                        items.append(item)
                except Exception as e:
                        print '--->Exception:',e
                        pass

        print u'-------------结束抓取页面-------------'
        filename="./out/items" +time.strftime('%Y%m%d %H%M%S', time.localtime(time.time()))+ '.out' 
        open(filename, 'wb').write(str(items))
