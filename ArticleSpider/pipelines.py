# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
import psycopg2.extras
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class ArticleSpiderPipeline(object):

    def process_item(self, item, spider):
        return item


class JsonExporterPipeline(object):

    def __init__(self):
        self.file = open('article.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class PostgresTwistedPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        db_pool = adbapi.ConnectionPool("psycopg2", **dict(
            host=settings['POSTGRES_HOST'],
            port=settings['POSTGRES_PORT'],
            database=settings['POSTGRES_DATABASE'],
            user=settings['POSTGRES_USER'],
            password=settings['POSTGRES_PASSWORD'],
            cursor_factory=psycopg2.extras.DictCursor,
        ))
        return cls(db_pool)

    def __init__(self, db_pool):
        self.db_pool = db_pool

    def process_item(self, item, spider):
        query = self.db_pool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        # 执行数据插入
        insert_sql = """INSERT INTO article(url_object_id, url, title, tags, front_image_url, front_image_path, comment_nums, 
                    fav_nums, praise_nums, create_date, content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(insert_sql, (item["url_object_id"], item["url"], item["title"], item["tags"],
                       item["front_image_url"], item["front_image_path"], item["comment_nums"], item["fav_nums"],
                       item["praise_nums"], item["create_date"], item["content"]))

    def handle_error(self, failure, item, spider):
        # 插入异常处理
        print(failure.value.pgerror)


class ArticleImagesPipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        if 'front_image_url' in item:
            for ok, value in results:
                if 'path' in value:
                    item['front_image_path'] = value['path']
        return item
