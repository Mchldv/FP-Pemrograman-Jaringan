import socket
import select
import sys
import os
import threading

fileport = open('httpserver.conf', 'r')
port = int(fileport.read())
print port
fileport.close()

# print port

root = os.getcwd()


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = '127.0.0.1'
        #self.host = '10.151.43.221'
        serveraddr = (self.host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(serveraddr)
        print self.sock

        # self.threads=[]
        self.sock.listen(5)

    def listen(self):
        try:
            while True:
                client_socket, client_address = self.sock.accept()
                print client_socket.getpeername(), 'is connected'
                client_socket.settimeout(300)
                threading.Thread(target=self.ReceiveData, args=(client_socket, client_address)).start()
        except KeyboardInterrupt:
            self.sock.close()
            sys.exit(0)

    def ReceiveData(self, client_socket, client_address):
        while (True):
            data = client_socket.recv(1024)
            print data
            if data == '':
                break
            else:
                request_header = data.strip().split('\r\n')
                #content_length = request_header[2].split(': ')[1]
                #print content_length
                request_file = request_header[0].split()[1]
                method = request_header[0].split()[0]

                if method == 'GET':
                    print "hear"
                    self.do_get(client_socket, request_file)
                elif method == 'HEAD':
                    print "head"
                    self.do_head(client_socket, request_file)
                elif method == 'POST':
                    post_data = data.strip().split('\r\n\r\n')[1]
                    self.do_post(client_socket, post_data)
                    

    def do_post(self, client_socket, data):
        #print data
        
        #not_found = 0

        message ='Berhasil kirim ' + data
        content_length = len(message)
        response_header = 'HTTP/1.1 200 OK\r\nContent-Length: ' + str(content_length) + '\r\n\r\n'
        client_socket.sendall(response_header+message);
        
        

        #for a in 

    def do_get(self, client_socket, request_file):
        print request_file
        not_found = 0

        cur_file_name = request_file.strip().split('/')[-1]
        if cur_file_name == '':
            cur_dir = request_file
        else:
            cur_dir = request_file[:-len(cur_file_name)]

        print 'file_name : ' + cur_file_name
        print 'cur_dir : ' + cur_dir

        os.chdir(root + cur_dir)
        #        print os.getcwd()

        if request_file == '/pages/' or request_file == '/pages' or request_file == '/dataset/a.html':
                    not_found = 2
        elif cur_file_name == '':
            #            os.chdir(root+cur_dir)
            if 'index.html' in os.listdir(os.getcwd()):
                f = open('index.html', 'r')
                response_data = f.read()
                f.close()

                content_length = len(response_data)
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                    content_length) + '\r\n\r\n'
            else:
                first = 1
                response_data = ''
                for name in os.listdir(os.getcwd()):
                    path = os.path.join(cur_file_name, name)
                    add_content = '<a href="' + path + '"> \\' + name + '</a><br>'
                    if (first == 1):
                        response_data = add_content
                        first = 0
                    else:
                        response_data += add_content
                content_length = len(response_data)
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                    content_length) + '\r\n\r\n'
        elif os.path.isfile(cur_file_name):
            f = open(cur_file_name, 'rb')
            response_data = f.read()
            f.close()
            content_length = len(response_data)
            if (cur_file_name.split('.')[1] == 'html'):
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                    content_length) + '\r\n' + 'File-Name: ' + cur_file_name + '\r\n\r\n'
            else:
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: media/html; charset=UTF-8\r\nContent-Length: ' + str(
                    content_length) + '\r\n' + 'File-Name: ' + cur_file_name + '\r\n\r\n'
        elif os.path.isdir(cur_file_name):
            first = 1
            response_data = ''
            for name in os.listdir(cur_file_name):
                path = os.path.join(cur_file_name, name)
                add_content = '<p><a href="' + path + '">' + name + '</a></p>'
                if (first == 1):
                    response_data = add_content
                    first = 0
                else:
                    response_data += add_content
            content_length = len(response_data)
            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                content_length) + '\r\n\r\n'
        else:
            not_found = 1
        if (not_found == 1):
            os.chdir(root)
            f = open('pages/404.html', 'r')
            response_data = f.read()
            f.close()

            content_length = len(response_data)
            response_header = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                content_length) + '\r\n\r\n'
        elif(not_found == 2):
                    os.chdir(root)
                    f = open('pages/403.html','r')
                    response_data = f.read()
                    f.close()
                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 403 FORBIDDEN\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: '+ str(content_length) + '\r\n\r\n'

        client_socket.sendall(response_header + response_data)
    
    def do_head(self, client_socket, request_file):
        print request_file
        not_found = 0

        cur_file_name = request_file.strip().split('/')[-1]
        if cur_file_name == '':
            cur_dir = request_file
        else:
            cur_dir = request_file[:-len(cur_file_name)]

        print 'file_name : ' + cur_file_name
        print 'cur_dir : ' + cur_dir

        os.chdir(root + cur_dir)
        #        print os.getcwd()

        if request_file == '/pages/' or request_file == '/pages' or request_file == '/dataset/a.html':
                    not_found = 2
        elif cur_file_name == '':
            #            os.chdir(root+cur_dir)
            if 'index.html' in os.listdir(os.getcwd()):
                f = open('index.html', 'r')
                response_data = f.read()
                f.close()

                content_length = len(response_data)
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                    content_length) + '\r\n\r\n'
            else:
                first = 1
                response_data = ''
                for name in os.listdir(os.getcwd()):
                    path = os.path.join(cur_file_name, name)
                    add_content = '<a href="' + path + '"> \\' + name + '</a><br>'
                    if (first == 1):
                        response_data = add_content
                        first = 0
                    else:
                        response_data += add_content
                content_length = len(response_data)
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                    content_length) + '\r\n\r\n'
        elif os.path.isfile(cur_file_name):
            f = open(cur_file_name, 'rb')
            response_data = f.read()
            f.close()
            content_length = len(response_data)
            if (cur_file_name.split('.')[1] == 'html'):
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                    content_length) + '\r\n' + 'File-Name: ' + cur_file_name + '\r\n\r\n'
            else:
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: media/html; charset=UTF-8\r\nContent-Length: ' + str(
                    content_length) + '\r\n' + 'File-Name: ' + cur_file_name + '\r\n\r\n'
        elif os.path.isdir(cur_file_name):
            first = 1
            response_data = ''
            for name in os.listdir(cur_file_name):
                path = os.path.join(cur_file_name, name)
                add_content = '<p><a href="' + path + '">' + name + '</a></p>'
                if (first == 1):
                    response_data = add_content
                    first = 0
                else:
                    response_data += add_content
            content_length = len(response_data)
            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                content_length) + '\r\n\r\n'
        else:
            not_found = 1
        if (not_found == 1):
            os.chdir(root)
            f = open('pages/404.html', 'r')
            response_data = f.read()
            f.close()

            content_length = len(response_data)
            response_header = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                content_length) + '\r\n\r\n'
        elif(not_found == 2):
                    os.chdir(root)
                    f = open('pages/403.html','r')
                    response_data = f.read()
                    f.close()
                    content_length = len(response_data)
                    response_header = 'HTTP/1.1 403 FORBIDDEN\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: '+ str(content_length) + '\r\n\r\n'

        client_socket.sendall(response_header)


    

        


if __name__ == "__main__":
    ThreadedServer('', port).listen()
    # s= ThreadedServer()
    # s.listen()
