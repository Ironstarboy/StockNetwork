import pymysql
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


def select(sql):
    db = connect()
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    results=None
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        print(e)
        print('select error')
    db.close()
    return results


def insert(sql):
    db = connect()
    cursor = db.cursor()
    try:
       cursor.execute(sql)
       db.commit()
    except:
       # 如果发生错误则回滚
       db.rollback()
       print('insert error')
    db.close()


def create(sql,tableName):
    db=connect()
    cursor = db.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS {}".format(tableName))
        cursor.execute(sql)
    except:
        print('create error')
    db.close()

