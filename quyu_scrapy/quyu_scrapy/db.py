# coding=utf-8
# coding=utf-8
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

'''
user = User(name='a')
session.add(user)
user = User(name='b')
session.add(user)
user = User(name='a')
session.add(user)
user = User()
session.add(user)
session.commit()
query = session.query(User)
print query # 显示SQL 语句
print query.statement # 同上
for user in query: # 遍历时查询
    print user.name
print query.all() # 返回的是一个类似列表的对象
print query.first().name # 记录不存在时，first() 会返回 None
# print query.one().name # 不存在，或有多行记录时会抛出异常
print query.filter(User.id == 2).first().name
print query.get(2).name # 以主键获取，等效于上句
print query.filter('id = 2').first().name # 支持字符串
query2 = session.query(User.name)
print query2.all() # 每行是个元组
print query2.limit(1).all() # 最多返回 1 条记录
print query2.offset(1).all() # 从第 2 条记录开始返回
print query2.order_by(User.name).all()
print query2.order_by('name').all()
print query2.order_by(User.name.desc()).all()
print query2.order_by('name desc').all()
print session.query(User.id).order_by(User.name.desc(), User.id).all()
print query2.filter(User.id == 1).scalar() # 如果有记录，返回第一条记录的第一个元素
print session.query('id').select_from(User).filter('id = 1').scalar()
print query2.filter(User.id > 1, User.name != 'a').scalar() # and
query3 = query2.filter(User.id > 1) # 多次拼接的 filter 也是 and
query3 = query3.filter(User.name != 'a')
print query3.scalar()
print query2.filter(or_(User.id == 1, User.id == 2)).all() # or
print query2.filter(User.id.in_((1, 2))).all() # in
query4 = session.query(User.id)
print query4.filter(User.name == None).scalar()
print query4.filter('name is null').scalar()
print query4.filter(not_(User.name == None)).all() # not
print query4.filter(User.name != None).all()
print query4.count()
print session.query(func.count('*')).select_from(User).scalar()
print session.query(func.count('1')).select_from(User).scalar()
print session.query(func.count(User.id)).scalar()
print session.query(func.count('*')).filter(User.id > 0).scalar() # filter() 中包含 User，因此不需要指定表
print session.query(func.count('*')).filter(User.name == 'a').limit(1).scalar() == 1 # 可以用 limit() 限制 count() 的返回数
print session.query(func.sum(User.id)).scalar()
print session.query(func.now()).scalar() # func 后可以跟任意函数名，只要该数据库支持
print session.query(func.current_timestamp()).scalar()
print session.query(func.md5(User.name)).filter(User.id == 1).scalar()
query.filter(User.id == 1).update({User.name: 'c'})
user = query.get(1)
print user.name
user.name = 'd'
session.flush() # 写数据库，但并不提交
print query.get(1).name
session.delete(user)
session.flush()
print query.get(1)
session.rollback()
print query.get(1).name
query.filter(User.id == 1).delete()
session.commit()
print query.get(1)
'''

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class AreaModel(Base):
    __tablename__ = 'tb_area_spider'

    def __init__(self, name, code):
        Base.__init__(self)
        self.name = name
        self.code = code

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(length=100))
    code = Column(String(length=100))
    level = Column(Integer(), nullable=False)


class UrlModel(Base):
    __tablename__ = 'tb_url_spider'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    url = Column(String(length=2000))
    html = Column(Text())


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:123@localhost:3306/test_x?charset=utf8')
Base.metadata.create_all(engine)
print('创建数据表')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


def add_area(name, code, level):
    session = DBSession()
    try:
        data = AreaModel(name, code)
        data.level = level
        session.add(data)
        session.commit()
    finally:
        session.close()


def add_url(url, html):
    session = DBSession()
    try:
        data = UrlModel()
        data.url = url
        data.html = html
        session.add(data)
        session.commit()
    finally:
        session.close()


def read_url(url):
    session = DBSession()
    try:
        return session.query(UrlModel).filter(UrlModel.url == url.lower()).limit(1).all()
    finally:
        session.close()


def all_data():
    session = DBSession()
    try:
        return session.query(AreaModel).limit(1000).all()
    finally:
        session.close()


def prepare_data(d):
    for x in [8, 6, 3]:
        if d.endswith('0' * x):
            return d[0:len(d) - x]
    print('not handle', d)
    return d


def prepare_parent(d):
    return d


def handle():
    data = all_data()
    data = [{'name': x.name, 'code': prepare_data(x.code)} for x in data]
    for m in data:
        m['parent'] = m['code']
    print(data)
    pass

# handle()
