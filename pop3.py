# -*- coding: cp936 -*-
# pop3.py  
  
import poplib
import cStringIO
import email
import base64
import os
import config

flag = 0

pop3_server = config.read('pop', 'server')
user_name = config.read('usr', 'name')
password = config.read('usr', 'password')

# ��ȡ����
def parseEmail(msg,path):
    mailContentDict = {}
    fileList = []
    mailContent = ''
    for part in msg.walk():
        #if not part.is_multipart():
        contenttype = part.get_content_type()
        filename = part.get_filename()
        if filename and contenttype=='application/octet-stream':
            fullpath = os.path.join(path,filename)
            #save
            if not os.path.exists(path):
                os.mkdir(path)
            if os.path.exists(fullpath):
                print filename," existed"
            else:
                f = open(fullpath,'wb')
                print filename," creat"
                f.write(base64.decodestring(part.get_payload()))
                f.close()

# pop3ȡ��
def pop(path):
    M = poplib.POP3(pop3_server)  
    M.user(user_name)  
    M.pass_(password)  
    # ����Ϊ1���ɲ鿴��pop3�������ύ��ʲô����  
    #M.set_debuglevel(1)  
      
    # ��ȡ��ӭ��Ϣ  
    serverWelcome = M.getwelcome()  
    print serverWelcome  
      
    # ��ȡһЩͳ����Ϣ  
    emailMsgNum, emailSize = M.stat()  
    #print 'email number is %d and size is %d'%(emailMsgNum, emailSize)  
      
    # �����ʼ�������ӡ��ÿ���ʼ��ı���  
    for i in range(emailMsgNum):
        m = M.retr(i+1)
        buf = cStringIO.StringIO()
        for piece in m[1]:
            print >>buf,piece
        buf.seek(0)
        for piece in m[1]:
            #print piece
            if piece.startswith('From'):
                addrfrom = str(piece)
                try:
                    addrfrom.index(config.read('pop', 'addr'))
                    start_addr = addrfrom.index('<')
                    end_addr = addrfrom.index('>')
                    flag = 1
                    #print addrfrom[start_addr + 1 : end_addr]
                except ValueError:
                    flag = 0
                    #print '\t' + piece
                    continue
                break
            #if piece.startswith('Subject'):
                #print '\t' + piece
            #if piece.startswith('Date'):
                #print '\t' + piece
        if (flag == 1):
             mail_message = email.message_from_file(buf)
             parseEmail(mail_message,path)
    M.quit()  


            
