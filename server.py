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
    def ReceiveData(self, client_socket, client_address):
        while (True):
            try:
                data = client_socket.recv(1024)
                print data
                if data == '':
                    break
                else:
                    request_header = data.strip().split('\r\n')
                    # content_length = request_header[2].split(': ')[1]
                    # print content_length
                    request_file = request_header[0].split()[1]
                    method = request_header[0].split()[0]

                    if method == 'GET':
                        print "hear"
                        self.do_get(client_socket, request_file)
                    elif method == 'HEAD':
                        print "head"
                        self.do_head(client_socket, request_file)
                    elif method == 'POST':
                        print "post\n\n"
                        content_length = request_header[2].split(': ')[1]
                        post_data = data.strip().split('\r\n\r\n')[1]
                        self.do_post(client_socket, post_data, content_length)
                    else:
                        os.chdir(root)
                        f = open('pages/500.html', 'r')
                        message = f.read()
                        f.close()
                        #message = message + '\nPOST parameter is too long/Content-Length is wrong'
                        content_length = len(message)
                        response_header = 'HTTP/1.1 500 INTERNAL SERVER ERROR\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(content_length) + '\r\n\r\n'
                        client_socket.sendall(response_header+message)
            except:
                break
         
                    

    def do_post(self, client_socket, data, content_length):
        #print data

        #print 'content_length = ' + content_length + '\n'
        #print 'data keterima = ' + str(len(data)) + '\n'
        #not_found = 0

        if content_length == str(len(data)):
            message ='Data yang diterima: ' + data
            content_length = len(message)
            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(content_length) + '\r\n\r\n'
            
        else:
            #message ='Server Error'
            #content_length = len(message)
            os.chdir(root)
            f = open('pages/500.html', 'r')
            message = f.read()
            f.close()
            #message = message + '\nPOST parameter is too long/Content-Length is wrong'
            content_length = len(message)
            response_header = 'HTTP/1.1 500 INTERNAL SERVER ERROR\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(content_length) + '\r\n\r\n'
        
        client_socket.sendall(response_header+message)

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

        if '/pages' in request_file or request_file == '/dataset/a.html':
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
            response_data = '0'
            response_header = 'HTTP/1.1 301 MOVED PERMANENTLY\r\nContent-Type: text/html; charset=UTF-8\r\n' + 'Location: ' + request_file + cur_dir + '\r\nContent-Length: 0' + '\r\n\r\n'
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
        elif (not_found == 2):
            os.chdir(root)
            f = open('pages/403.html', 'r')
            response_data = f.read()
            f.close()
            content_length = len(response_data)
            response_header = 'HTTP/1.1 403 FORBIDDEN\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                content_length) + '\r\n\r\n'

        client_socket.sendall(response_header + response_data)

    def do_head(self, client_socket, request_file):
        global response_header, response_header
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

        if '/pages' in request_file or request_file == '/dataset/a.html':
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
                    if first == 1:
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
            if cur_file_name.split('.')[1] == 'html':
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
        if not_found == 1:
            os.chdir(root)
            f = open('pages/404.html', 'r')
            response_data = f.read()
            f.close()

            content_length = len(response_data)
            response_header = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                content_length) + '\r\n\r\n'
        elif not_found == 2:
            os.chdir(root)
            f = open('pages/403.html', 'r')
            response_data = f.read()
            f.close()
            content_length = len(response_data)
            response_header = 'HTTP/1.1 403 FORBIDDEN\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: ' + str(
                content_length) + '\r\n\r\n'

        client_socket.sendall(response_header)


if __name__ == "__main__":
    server_host = '127.0.0.1'
    serveraddr = (server_host, port)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(serveraddr)
    print server_sock

    # self.threads=[]
    server_sock.listen(5)

    input_socket = [server_sock]
    try: 
        while True:
            read_ready, write_ready, exception = select.select(input_socket, [], [])
            
            for sock in read_ready:
                server_sock.listen(5)
                if sock == server_sock:
                    client_socket, client_address = server_sock.accept()
                    #client_socket.settimeout(60)
                    #ThreadedServer.ReceiveData(target = self.ReceiveData,args = (client_socket,client_address)).start()
                    input_socket.append(client_socket)
                    #print "server_socket:"+str(sock)
                else:
                    t1 = threading.Thread(target=ThreadedServer().ReceiveData, args=(client_socket,client_address))
                    t1.start()
##                    s= ThreadedServer()
##                    s.ReceiveData(client_socket,client_address).start()
                    #print "client_socket:"+str(sock)

                    
    except KeyboardInterrupt:
        server_sock.close()
        sys.exit(0)
    # 
