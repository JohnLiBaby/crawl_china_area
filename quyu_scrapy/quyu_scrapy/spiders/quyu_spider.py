# coding=utf-8
import scrapy
import os
from quyu_scrapy import db, html_parser, url_filter


class AreaSpider(scrapy.Spider):
    name = "area"

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.data_path = os.path.join('d:\\', '_data')
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)

    def start_requests(self):
        urls = [
            'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/index.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print(dir(response))
        html = response.text
        db.add_url(response.url.lower(), html)
        # 提取数据
        for data in html_parser.parse_area(response):
            if data:
                yield data
        # 下一页
        for url in response.css('a::attr(href)'):
            next_page = response.urljoin(url.extract())
            next_page = url_filter.filter_url(next_page.lower())
            if next_page:
                print('下一页', next_page, '深度', response.meta['depth'])
                yield response.follow(url, callback=self.parse)
