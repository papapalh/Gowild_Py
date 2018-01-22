# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from gowild.items import JobBoleArticleItem

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # 获取文章的具体URL,并解析文章,爬取数据
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")

        # 1:08

        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=post_url, meta={"front_image":image_url},callback=self.parse_detail)

        # 提取下一页URL
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        # if next_url:
            # yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        # 实例化ITEM
        article_item = JobBoleArticleItem()

        # 爬取页面
        front_image_url = response.meta.get("front_image", "")
        re_title = response.css(".entry-header h1").extract_first()
        re_time = response.css(".entry-meta-hide-on-mobile::text").extract_first().strip()
        re_time = re.match(".*?([2]{1}[0-9]{3}[/][0-9]{2}[/][0-9]{2})",re_time).group(0)
        re_content = response.xpath("//div[@class='entry']").extract_first()

        # ITEM赋值
        article_item['title'] = re_title
        article_item['time'] = re_time
        article_item['content'] = re_content
        article_item['front_image_url'] = [front_image_url]

        yield article_item
