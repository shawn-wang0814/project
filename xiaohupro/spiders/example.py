import scrapy
from xiaohupro.items import XiaohuproItem
from lxml import etree
import requests
# def get_urls():
#     urls = []
#     for i in range(100):
#         url = 'https://www.ruyile.com/nice/?f=3&p=%s' % str(i + 1)
#         print(url)
#         urls.append(url)
#     return urls


class ExampleSpider(scrapy.Spider):
    name = 'example'
    # allowed_domains = ['example.com']
    start_urls = ["https://www.ruyile.com/nice/?f=3"]
    url = "https://www.ruyile.com/nice/?f=3&p=%s"
    p_num = 2

    def src_parse(self,res):
        src_ps = res.xpath("/html/body/div[4]/div[1]/div/div[4]/p[@align='center']")
        src_urls = []
        for p in src_ps:
            src_url = p.xpath("./img/@src")
            src_urls.append(src_url)
        return src_urls


    def parse(self, response):
        a_list = response.xpath("/html/body/div[4]/div[1]/div[2]/div")
        for a in a_list:
            if a != None:
                a_herf = a.xpath("./div[2]/a/@href").extract_first()
                a_text = a.xpath("./div[2]/a/text()").extract_first()
                print("a.href: ",a_herf)
                print("a.text: ",a_text)
                item = XiaohuproItem()
                img_url = "https://www.ruyile.com/" + a_herf
                # resp = requests.get(img_url).text

                # item['src'] = scrapy.Request(img_url,callback=self.src_parse)
                resp = etree.HTML(requests.get(img_url).text)
                item['src'] = self.src_parse(resp)
                yield item
            else:
                continue
            while self.p_num <= 20:
                new_url = format(self.url % self.p_num)
                self.p_num += 1
                yield scrapy.Request(url=new_url,callback=self.parse)



