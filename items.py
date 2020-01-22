import requests,re
import alchemy as db
from lxml import etree

class wanacg(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
    }
    proxies = {
        'http': 'http://localhost:1080',
        'https': 'https://localhost:1080'
    }
    link_set = set()
    def req(self, page_num):
        link_set = db.db_session.query(db.Torrant.link).all()
        for x in link_set:
            for y in x:
                self.link_set.add(y)
        del link_set
        try:
            url = 'https://wnacg.org/albums-index-cate-9.html'
            items = []
            for page in range(page_num):      #此处控制页数
                goUrl = "https://wnacg.org/albums-index-" + "page-" + str(page+1) + "-cate-9.html"
                response = requests.get(goUrl, headers=self.headers,proxies=self.proxies,timeout=10)
                selector = etree.HTML(response.text)
                object = selector.xpath('//ul[@class="cc"]/li')
                for x in object:
                    item = {}
                    item['link'] = 'https://wnacg.org' + x.xpath('div[@class="pic_box"]/a/@href')[0]  #详情页url
                    item['image'] = 'http:' + x.xpath('div[@class="pic_box"]/a/img/@src')[0]  #封面图片url
                    item['title'] = x.xpath('div[@class="info"]/div[@class="title"]/a/text()')[0]  #标题
                    item['num'] = re.search('[0-9]{5}', item['link']).group()  #编号
                    item['gallary'] = 'https://wnacg.org/photos-gallery-aid-' + str(item['num']) + '.html'  #漫画总图控制信息url
                    items.append(item)

            for item in items:
                print(item)
                response = requests.get(item['link'], headers=self.headers,proxies=self.proxies,timeout=10)
                selector = etree.HTML(response.text)
                item['download'] = 'https://wnacg.org' + selector.xpath('//div[@class="asTBcell uwthumb"]/a[3]/@href')[0]  #下载页url
                
            for item in items:
                print(item)
                if item['download'] in self.link_set:
                    item['bit'] = None
                else:
                    response = requests.get(item['download'], headers=self.headers,proxies=self.proxies,timeout=10)
                    selector = etree.HTML(response.text)
                    item['bit'] = selector.xpath('//a[@class="down_btn"]/@href')[0]  #下载url
            
            return items

        except Exception as e:
            print("Failed to get type page")
            print(e)
        
        


if __name__ == '__main__':
    items = wanacg().req(1)  #请求并获取item
    wanacg().pipeline(items)  #将items存放到数据库
    wanacg().download(item)   #将items中每个漫画下载到本地某路径下

