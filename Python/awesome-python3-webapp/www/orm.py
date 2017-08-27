#!/usr/bin/env python3
# -*- oding: utf-8 -*-

import asyncio, logging

import aiomysql

def log(sql, args=()):
    logging.info('SQL: %s' % sql)

async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
            host=kw.get('host', 'localhost'),
            port=kw.get('port', 3306),
            user=kw['user'],
            password=kw['password'],
            db=kw['db'],
            charset=kw.get('charset', 'utf8'),
            autoommit=kw.get('autocommit', True), #自动提交事务
            maxsize=kw.get('maxsize', 10),        #池中最多有10个链接对象
            minsize=kw.get('minsize', 1),
            loop=loop
            )

async def select(sql, args, size=None): #size可以决定取几条
    log(sql, args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
        # 用参数替换而非字符串拼接可以防止sql注入
            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
        logging.info('rows returned: %s' %len(rs))
        return rs

async def execute(sql, args, autocommit=True):
    log(sql)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                affected = cur.rowcount
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ','.join(L)


#字段类的实现
class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name # 字段名
        self.column_type = column_type # 字段数据类型
        self.primary_key = primary_key # 是否是主键
        self.default = default # 有无默认值

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.name__name__,self.column_type, self.name)


class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().init_(name,ddl,primary_key,default)


class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)
        

class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)

class TextField(Field):

    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


class ModelMetaclass(type):
    # 元类必须实现__new__方法，当一个类指定通过某元类来创建，就会调用该元类的__new__方法
    # 该方法接收4个参数
    # cls为当前准备创建的类的对象
    # name为类的名字，创建User类，则name便是User
    # base类继承的父类集合，创建User类，则base便是Model
    # attrs为类的属性/方法集合，创建User类，则attrs便是一个包含User类属性的dict
    def __new__(cls, name, bases, attrs):
        # 因为Model类是基类，所以排除掉，如果你print(name)的话，会依次打印出Model，User,Blog
        # 即所有的Model子类，因为这些子类通过Model间接继承元类
        if name=="Model":
            return type.__new__(cls, name, bases, attrs)
        # 取出表名，默认与类的名字相同
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table:%s)' % (name, tableName))
        # 用于存储所有的字段，以及字段值
        mappings = dict()
        # 仅用来存储非主键以外的其它字段，而且只存key
        fields = []
        # 仅保存主键的key
        primaryKey = None
        # 注意这里attrs的key是字段名， value是字段实例，不是字段的具体值
        # 比如User类的id=StringField(...) 这个value就是这个StringField的一个实例,而不是
        # 实例化的时候传进去的具体的id值
        for k,v in attrs.items():
            # attrs同时还会拿到一些其它系统提供的类属性，我们只处理自定义的类属性，所以
            # 判断一下isinstance方法用于判断v是否是一个Field
            if isinstance(v, Field):
                logging.info(' found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    if primaryKey:
                        raise ValueError("Douplicate primary key for field :%s" % key)
                    primaryKey=k
                else:
                    fields.append(k)

        # 保证必须有一个主键
        if not primaryKey:
            raise ValueError("Primary key not found")

        # 这里的目的是去除类属性，为什么要去除呢，因为我想知道的信息已经记录下来了
        # 去除之后，就访问不到类属性了
        # 记录到了mappings,fields,等变量里，而我们实例化的时候,如
        # user=User(id='10001')，为了防止这个实例变量与类属性冲突，所以将其去掉
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        # 以下都是要返回的东西了，刚刚记录下的东西，如果不返回给这个类，又谈得上什么动态创建呢
        # 到此，动态创建便比较清晰了，各个子类根据自己的字段名不同，动态创建自己
        # 下面通过attrs返回的东西，在子类里都能通过实例拿到，如self
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName
        attrs['__primaryKey__'] = primaryKey
        attrs['__fields__'] = fields
        # 只是为了Model编写方便，放在元类里和放在Model里都可以
        attrs['__select__'] = "select %s ,%s from %s " % (primaryKey,','.join(map(lambda f: '%s' % (mappings.get(f).name or f ),fields )),tableName)
        attrs['__update__'] = "update %s set %s where %s=?"  % (tableName,', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)),primaryKey)
        attrs['__insert__'] = "insert into %s (%s,%s) values (%s);" % (tableName,primaryKey,','.join(map(lambda f: '%s' % (mappings.get(f).name or f),fields)),create_args_string(len(fields)+1))
        attrs['__delete__'] = "delete from %s where %s= ? ;" % (tableName,primaryKey)
        return type.__new__(cls,name,bases,attrs)


# 让Model继承，主要是为了具备dict所有的功能，如get方法
# metaclass 指定了Model类的元类为ModelMetaClass
class Mode(dict, metaclass = ModelMetaclass):

    def __init(self, **kw):
        super(Moder, self).__init__(**kw)

    # 实现__getattr__与__setattr__方法，可以使引用属性像引用普通字段一样 如self['id']
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
    
    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value
    # 一处异步，处处异步，所以这些方法都必须是一个协程

    # 类方法
    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause. '
        sql=[cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.exend(limit)
            else:
                raise ValueError('Invalid limit value: %S' % str(limit))
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    async def findNumer(cls, selectField, where=None, args=None):
        ' find number by select and where '
        sql = ['select %s _num_ from `%s` ' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']


    @classmethod
    async def find(cls, pk):
        ' find object by primark key '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primaryKey__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0]) # 返回的是一个实例对象引用

    
    # 下面 self.__mappings__, self.__insert__等变量是根据对应表的字段不同而动态创建的
    async def save(self):
        args=list(map(self.getValueOrDefault,self.__mappings__))
        args.append(self.getValueOrDefault(self.__primaryKey__))
        rows = await execute(self.__insert__,args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)


    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primaryKey__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)


    async def remove(self):
        args = [self.getValue(self.__primaryKey__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows :%s' % rows)

