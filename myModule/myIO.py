import os


def readFile(filename):
    content = ''
    encodings = ['utf-8', 'GBK', 'gb2312']
    index = 0
    while 1:
        if content != '' or index == len(encodings):
            break
        try:
            f = open(filename, 'r+', encoding=encodings[index])
            content = f.read()
            f.close()
            break
        except:
            pass
            # print('{} {}编码失败，正在尝试下一种编码'.format(filename,encodings[index]))
        finally:
            index += 1
    if content == '':
        print('{}读取失败'.format(filename))
    return content

def mkDir(dirPath):
    # pic/1.png 1.png会被创建成文件夹
    dirname=os.path.dirname(dirPath)
    if not os.path.exists(dirname):
        os.makedirs(dirname) # 可以递归创建 ，即可以创建多层目录结构
        print('dir {}创建成功'.format(dirname))
    else:
        print('dir {}已存在'.format(dirname))
    return dirPath

# 获取文件列表，该目录下放着一同个类别的文档,数量为几百份。不进行递归获取
def getFileNameList(path):
    filelist = []
    files = os.listdir(path)
    for f in files:
        if (f[0] == '.'):
            pass
        else:
            filelist.append(f)
    return filelist

def delFileByDir(dir):
    files=getFileNameList(dir)
    for fileNameExt in files:
        os.remove(dir+'\\'+fileNameExt)
        print('{} is deleted'.format(fileNameExt))


def getFileNameExt(filePath):
    """ 输入文件路径，输出文件名以及后缀 """
    return os.path.basename(filePath)

# 可递归获取置顶目录下的文件路径
def recusiveGetFilePathList(dir):
    res=[]
    import os
    fileNames=[]
    for root, dirs, files in os.walk(dir):
        for file in files:
            res.append(os.path.join(root, file))
        fileNames.extend(files)
    return res,fileNames


def saveText(filePath, content:str, mode='w'):
    with open(filePath, mode,encoding='utf-8') as f:
        f.write(content)


import pickle
def dumpVar(var,filePath):
    if not os.path.exists(filePath):
        dirname=os.path.dirname(filePath)
        mkDir(dirname)
        with open(filePath,'wb') as f:
            pickle.dump(var, f)
            print(f'已保存至{filePath}')



def loadVar(filePath):
    with open(filePath,'rb') as f:
        res=pickle.load(f)
    return res

def readBits(filePath):
    res=None
    with open(filePath,'rb') as f:
        res=f.read()
    return res

import time
def timer(func):
    # 函数计时器
    def wrapper(*args, **kw):
        local_time = time.time()
        print(f'\033[37m[{func.__name__}] is running',end=': ')
        res=func(*args, **kw)
        t= time.time() - local_time
        print(f'[{func.__name__}] spent {t:.2f}s\033[0m')
        return res
    return wrapper