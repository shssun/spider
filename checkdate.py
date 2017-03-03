#! /usr/bin/env python  
# coding:utf-8  

import os, datetime
from collections import deque

# todo: 每个文件夹下, 按文件的时间倒序显示
# todo: 同步每个文件夹的时间为子文件夹中最近修改的文件时间

def bianlidir(dirlist, filelist):
    while dirlist:
        curdir = dirlist.popleft()
        print('正在遍历文件夹: ' + curdir)
        for file in os.listdir(curdir):
            path = curdir + file #全路径 文件夹+文件名
            if os.path.isfile(path):
                filelist.append(path)
            else:
                dirlist.append(path+'/')


def bianliflie(filelist):
    index = 0
    for file_ in filelist:
        index +=1
        #path = os.path.join(base_dir, filelist[i])
        timestamp = os.path.getmtime(file_)
        # print(timestamp)
        #ts1 = os.stat(path).st_mtime
        # print(ts1)

        date = datetime.datetime.fromtimestamp(timestamp)
        print("文件序号:", index, file_, '最近修改时间是:', date.strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    rootdir = 'F:/'
    dirlist = deque()
    filelist = deque()
    dirlist.append(rootdir)
    bianlidir(dirlist, filelist)
    bianliflie(filelist)