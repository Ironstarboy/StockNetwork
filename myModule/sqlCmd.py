import pymysql
import os
from warnings import filterwarnings
filterwarnings("error",category=pymysql.Warning) #指定过滤告警的类别为pymysql.Warning类

# 写成类应该可以持久化链接

def connect():
    db=pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='123123',
                       charset='utf8',
                       # cursorclass= pymysql.cursors.DictCursor,  # 返回值会变成字典格式
                       database='stockdata')
    return db


def select(query):
    db = connect()
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    results=None
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except pymysql.Warning as e:
        os.abort(50009, str({'error':e,'sql':query}))
    finally:
        db.close()
        return results


def insert(query):
    db = connect()
    cursor = db.cursor()
    try:
       cursor.execute(query)
       db.commit()
    except pymysql.Warning as e:
       # 如果发生错误则回滚
       os.abort(50009, str({'error': e, 'sql': query}))
       db.rollback()
    finally:
        db.close()


def create(query, tableName):
    db=connect()
    cursor = db.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS {}".format(tableName))
        cursor.execute(query)
    except:
        print('create error')
    db.close()

