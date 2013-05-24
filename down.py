#!/usr/bin/python
#-*- coding:utf-8 -*- 
# down.py
import sys,os
import time
import pop3
import config
import subprocess

flag = 0
Download_path = config.read('global','down')
BT_path = os.path.join(Download_path,'BT')
TXT_path = os.path.join(BT_path,'log.txt')
li = []
len_mx = 5

#遍历
def dir_fun(path,txt):
    for root,dirs,files in os.walk(path):
        for fn in files:
            #print(root,fn)
            if (fn != 'log.txt'):
                _verifyContent(txt,fn)
#查询
def search(path=None,txt=None):
    if not path or not txt:
        print('path or searchString is empty')
        return
    fobj = open(txt,'w')
    fobj.close()
    while True:
        dir_fun(path,txt)
        time.sleep(5)
        print('sleep')

#匹配
def _verifyContent(path,cont):
    global flag
    fobj = open(path,'r')
    lines = fobj.readlines()
    fobj.close()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\r','')
        lines[i] = lines[i].replace('\n','')
        if lines[i] == cont:
            flag = 1
            break
        i=i+1
    if flag == 1:
        # existed
        flag = 0
        return
    else:
        # download
        fobj=open(path,'a')
        fobj.write(cont+'\n')       
        _download(cont)
        fobj.close()
        return

def _download(cont):
    fileName, fileExtension = os.path.splitext(cont)
    if fileExtension == '.torrent':
         p = subprocess.Popen('lx download --bt '+os.path.join(BT_path,cont)+' --output-dir='+\
                              BT_path+' --delete'+' --continue', shell=True).pid
         print 'start download'
         li.append(p)
         while len(li) >= len_mx:
             _updateList(li)
             time.sleep(5)

def _updateList(li):

    for x in li:

        if x.returncode:

            li.remove(x)

            print 'remove'


if __name__ == "__main__":
    fobj = open(TXT_path,'a')
    fobj.close()
    os.system('lx login '+config.read('xunlei', 'name')+' '+\
              config.read('xunlei', 'password'))
    os.system('lx list')
    while True:
        while len(li) >= len_mx:
            _updateList(li)
            time.sleep(5)
        print time.ctime()
        pop3.pop(BT_path)
        dir_fun(BT_path,TXT_path)
        time.sleep(60*5)
