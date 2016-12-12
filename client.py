import socket               # Import socket module
from bs4 import BeautifulSoup

server_address = ('localhost', 80)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

#client_socket.send("Hello server!")
client_request=raw_input('URI : localhost')
request_header='GET '+client_request+' HTTP/1.1\r\nHost:localhost\r\n\r\n'
client_socket.send(request_header)
#print client_request
response=''

while 1:
    try:
        #print 'masuk'
        client_socket.settimeout(1)
        recv=client_socket.recv(1024)
        #print recv
        #print 'dalam while'
        if not recv or len(recv) == 0 :
            break
        response+=recv
    except socket.timeout:
        #more code
        break
    
response_header = response.split('\r\n')[1]
#print response_header + "\r\n"
content_type = response_header.split()[1]
#print content_type + "\r\n"

if content_type == 'application/force-download' :
    #fdfsdfsd
    content_disposition=response.split('\r\n')[2]
    filename=content_disposition.split('filename=')[1][1:-1]
    #print filename + '\r\n'
    f = open(filename,'wb+')
    isi_file = response.split('\r\n\r\n')[1]
    f.write(isi_file)
    f.close()
    print "Download Berhasil\r\n"
else :
    content = response.split('\r\n\r\n')[1]
    soup=BeautifulSoup(content, 'html.parser')
    isi_respon = soup. findAll('html')
    #print isi_respon
    for isi in isi_respon :
        print isi.text.strip()
client_socket.close                     # Close the socket when done
