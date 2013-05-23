#-*- coding:utf-8 -*- 
# down.py
import sys,os
import time
import pop3

num = 0
flag = 0
C_path = os.getcwd()
BT_path = os.path.join(C_path,'BT')
TXT_path = os.path.join(BT_path,'log.txt')

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
    global num
    global flag
    fobj = open(path,'r')
    fobjContent = fobj.readlines()
    fobj.close()
    for index,x in enumerate(fobjContent):
        if cont in x:
            flag = 1
            break
    if flag == 1:
        # existed
        flag = 0
        return
    else:
        # download
        fobj=open(path,'a')
        fobj.write(cont+'\n')       
        _download()
        fobj.close()
        return

def _download():
    print 'start download'

if __name__ == "__main__":
    fobj = open(TXT_path,'w')
    fobj.close()
    while True:
        print time.ctime()
        pop3.pop(BT_path)
        time.sleep(5)
        dir_fun(BT_path,TXT_path)
        time.sleep(60*5)
