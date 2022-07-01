# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy


# class XiaohuproPipeline:
#     def process_item(self, item, spider):
#         return item

class XiaoHuImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for src in item['src']:
            print(src)
            yield scrapy.Request(src[0])

    def file_path(self, request, response=None, info=None, *, item=None):
        img_name = request.url.split("/")[-1]

        return img_name

    def item_completed(self, results, item, info):
        return item