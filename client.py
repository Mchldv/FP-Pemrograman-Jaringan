import socket
import sys
import os
from bs4 import BeautifulSoup

fileport=open('httpserver.conf','r')
port=fileport.read()
fileport.close()

print int(port)

server_address = ('localhost', int(port))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(server_address)

try:
    while(1):
        URN=raw_input("masukkan nama_file : ")
        print URN
        client_socket.send('GET '+URN+' HTTP/1.1\r\nHost: 10.181.1.149:'+port+'\r\n\r\n')
        print 1;
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
    #client_socket.close()
    #client_socket.send('diterima')
    client_socket.close()
except KeyboardInterrupt:

    client_socket.close()

    sys.exit(0)
