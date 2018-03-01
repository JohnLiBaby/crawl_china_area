# coding=utf-8
from quyu_scrapy.items import QuyuScrapyItem
import time

_css = [
    {
        'cls': 'citytr',
        'col': [0, 1]
    },
    {
        'cls': 'countytr',
        'col': [0, 1]
    },
    {
        'cls': 'towntr',
        'col': [0, 1]
    },
    {
        'cls': 'villagetr',
        'col': [0, 2]
    },
]


def parse_area(response):
    level = 0
    for css in _css:
        level += 1
        cls = css['cls']
        col = css['col']
        for tr in response.css(f'tr.{cls}'):
            tds = tr.css('td').xpath('.//text()')
            name = tds[col[1]].extract()
            code = tds[col[0]].extract()
            if name and code:
                data = QuyuScrapyItem()
                data['name'] = name
                data['code'] = code
                data['level'] = level
                yield data
