# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.selector import Selector


'''



'''
  
class LJSpider(Spider):  
    name = 'LJ'

    
    allowed_domains = ['lianjia.com']  
    start_urls = [    'http://bj.lianjia.com/ershoufang/' ]
    start_urls = [    'http://bj.lianjia.com/ershoufang/dongcheng/pg1/' ]
    
    
    #allowed_domains = ["dmoz.org"]  
    #start_urls = [ "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"  ]

    #allowed_domains = ["baidu.com"]  
    #start_urls = [   "https://baidu.com/" ]

    
    def parse(self, response):  
        #filename = "bjlj"
        print '--------------------------'
        sel = Selector(response)
        houselist = sel.xpath('/html/body/div[4]/div[1]/ul/li')
        #houselist = sel.xpath('/html/body/div[4]/div[1]/ul/li')
        allout=[]
        i=1
        for house in houselist:
                    print i
                    i=i+1
                    try:
                        title = house.xpath('div[1]/div[1]/a/text()').pop().extract()
                        #print title.decode('gb18030')
                        print 'title:',title
                        allout.append(title)
                        #
                        '''<div class="houseInfo">
                            <span class="houseIcon"></span>
                            <a href="http://bj.lianjia.com/xiaoqu/1111027379462/" target="_blank" data-log_index="1" data-el="region">上龙西里 </a>
                            | 3室1厅 | 80.37平米 | 西南 东北 | 简装
                          </div>
                        '''
                        #print '=====>',house.xpath('div[1]/div[2]/div/a/@href').pop().extract()
                        #print '=====>',house.xpath('div[1]/div[2]/div/a/text()').pop().extract().decode('gb18030')
                        #链接地址
                        xiaoqu_link=house.xpath('div[1]/div[2]/div/a/@href').pop().extract()
                        print 'xiaoqu_link:',xiaoqu_link
                        fangzi_link=house.xpath('div[1]/div[1]/a/@href').pop().extract()
                        print 'fangzi_link:',fangzi_link
                        print house.xpath('div[1]/div[1]/a/@href').pop().extract()
                        area = house.xpath('div[1]/div[2]/div/text()').pop().extract().split('|')[2]
                        print 'area:',area
                        time = house.xpath('div[1]/div[4]/text()').pop().extract().split('/')[2]
                        print 'time:',time
                        price = house.xpath('div[1]/div[6]/div[1]/span/text()').pop().extract()
                        print 'price:',price,u'万'
                        '''
                        item['community'] = house.xpath('div[1]/div[2]/div/a/text()').pop()
                        item['model'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[1]
                        item['area'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[2]
                        item['focus_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[0]
                        item['watch_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[1]
                        item['time'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[2]
                        item['price'] = house.xpath('div[1]/div[6]/div[1]/span/text()').pop()
                        item['average_price'] = house.xpath('div[1]/div[6]/div[2]/span/text()').pop()
                        item['link'] = house.xpath('div[1]/div[1]/a/@href').pop()
                        item['city'] = response.meta["id1"]
                        self.url_detail = house.xpath('div[1]/div[1]/a/@href').pop()
                        item['Latitude'] = self.get_latitude(self.url_detail)
                        '''
                    except Exception as e:
                        print '--->Exception:',e
                        pass


        
        #open('allout', 'wb').write(response.body)
        #选择器
        #sel = Selector(response)
        #获取标题
        #print sel.xpath('//title')
        #print sel.xpath('//title/text()').extract()
        #print sel.xpath('//ul/li')
        #print sel.xpath('//ul/li/text()').extract()  
        print '--------------------------'
