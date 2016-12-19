import socket
import sys
import os
from bs4 import BeautifulSoup

fileport=open('httpserver.conf','r')
port=fileport.read()
fileport.close()

print int(port)

server_address = ('127.0.0.1', int(port))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(server_address)

def do_get_head():
    header=''
    while(True):
        a=client_socket.recv(1)
        #print a
        header+=a
        if '\r\n\r\n' in header:
            break
    print header
    content_length=header.strip().split('\r\n')[2].split()[1]
    #print content_length
    cur_content_length=0
    content=''
    while(cur_content_length<int(content_length)):
        content+=client_socket.recv(1)
        cur_content_length+=1
    #print content
    if '200' in header and 'media' in header:
        nama_file=header.strip().split('\r\n')[3].split()[1]
        print nama_file
        f=open(nama_file,"wb")
        f.write(content)
        f.close()
    else:
        soup=BeautifulSoup(content,"html.parser")
        print soup.getText()

def do_post():
    header=''
    while(True):
        a=client_socket.recv(1)
        #print a
        header+=a
        if '\r\n\r\n' in header:
            break
    print header
    content_length=header.strip().split('\r\n')[2].split()[1]
    #print content_length
    cur_content_length=0
    content=''
    while(cur_content_length<int(content_length)):
        content+=client_socket.recv(1)
        cur_content_length+=1
    print content

try:
    while(1):
        URN=raw_input("masukkan nama_file : ") #masukan nama file
        print "Masukan\r\n1 untuk GET\r\n2 untuk HEAD\r\n3 untuk POST" #membuat option
        method_option=raw_input("masukan method : ")
        method="GET"

        if method_option=='1':
            method="GET"
            client_socket.send(method+" "+URN+' HTTP/1.1\r\nHost: localhost:'+port+'\r\n\r\n')
            do_get_head()
        elif method_option=='2':
            method="HEAD"
            client_socket.send(method+" "+URN+' HTTP/1.1\r\nHost: localhost:'+port+'\r\n\r\n')
            do_get_head()            
        elif method_option=='3':
            method="POST"
            data="name=Michael&alamat=TC"
            length=str(len(data))
            client_socket.sendall(method+" "+URN+' HTTP/1.1\r\nHost: localhost:'+port+'\r\nContent-Length: '+length+'\r\n\r\n'+data)
            do_post()
        else:
            method="FOOT"
            client_socket.send(method+" "+URN+' HTTP/1.1\r\nHost: localhost:'+port+'\r\n\r\n')
            header=''
            while(True):
                a=client_socket.recv(1)
                header+=a
                if '\r\n\r\n' in header:
                    break
            content_length=header.strip().split('\r\n')[2].split()[1]
            #print content_length
            cur_content_length=0
            content=''
            while(cur_content_length<int(content_length)):
                content+=client_socket.recv(1)
                cur_content_length+=1
            print header+content
            
            
            
        
    #client_socket.close()
    #client_socket.send('diterima')
    client_socket.close()
except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)
