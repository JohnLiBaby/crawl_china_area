# coding=utf-8
from quyu_scrapy import db


def filter_url(url):
    if not url.lower().startswith('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016'.lower()):
        print('跳过', url)
        return None
    sp = url.split('/')
    if len(sp[len(sp) - 1].split('.')[0]) >= 9:
        print('跳过居委会', url)
        return None
    if len(db.read_url(url)) > 0:
        print('跳过已处理页面', url)
        return None
    return url
