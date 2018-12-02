# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy.http import Request

from ArticleSpider.items import JobBoleArticleItem, ArticleSpiderItemLoader
from ArticleSpider.utils.common import get_md5


class JobBoleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1、获取文章列表页的url并交给scrapy进行下载， 下载完成后交给解析函数进行具体字段的解析
        2、获取下一页的url并交给scrapy进行下载，下载完成 后交给 parse
        :param response:
        :return:
        """

        # 解析列表页中的所有文章url并交给scrapy进行下载
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={"front_image_url": parse.urljoin(response.url, image_url)},
                          callback=self.parse_detail)

        # 提取下一页的url并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        # 使用 item loader 封装解析结果
        item_loader = ArticleSpiderItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_css('create_date', 'p.entry-meta-hide-on-mobile::text')
        item_loader.add_css('praise_nums', '.vote-post-up h10::text')
        item_loader.add_css('fav_nums', 'span.bookmark-btn::text')
        item_loader.add_value('front_image_url', [response.meta.get("front_image_url", "")])
        item_loader.add_css('comment_nums', 'a[href="#article-comment"] span::text')
        item_loader.add_css('content', 'div.entry')
        item_loader.add_css('tags', 'p.entry-meta-hide-on-mobile a::text')
        yield item_loader.load_item()
