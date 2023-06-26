#encoding=utf-8
'''
Created on 2012-11-7

@author: Steven
http://www.lifeba.org
基于BaseHTTPServer的http server实现，包括get，post方法，get参数接收，post参数接收。
'''

"""
from http.server import HTTPServer,BaseHTTPRequestHandler
#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import io,shutil  
import urllib,time
import getopt,string

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.process(2)

    def do_POST(self):
        self.process(1)
        
    def process(self,type):
        
        content =""
        if type==1:#post方法，接收post参数
            datas = self.rfile.read(int(self.headers['content-length']))
            datas = urllib.unquote(datas).decode("utf-8", 'ignore')#指定编码方式
            datas = transDicts(datas)#将参数转换为字典
            if datas.has_key('data'):
                content = "data:"+datas['data']+"\r\n"
                
        if '?' in self.path:
            query = urllib.splitquery(self.path)
            action = query[0] 
                     
            if query[1]:#接收get参数
                queryParams = {}
                for qp in query[1].split('&'):
                    kv = qp.split('=')
                    queryParams[kv[0]] = urllib.unquote(kv[1]).decode("utf-8", 'ignore')
                    content+= kv[0]+':'+queryParams[kv[0]]+"\r\n"
                    
            #指定返回编码
            enc="UTF-8"  
            content = content.encode(enc)          
            f = io.BytesIO()  
            f.write(content)  
            f.seek(0)  
            self.send_response(200)  
            self.send_header("Content-type", "text/html; charset=%s" % enc)  
            self.send_header("Content-Length", str(len(content)))  
            self.end_headers()  
            shutil.copyfileobj(f,self.wfile)   

def transDicts(params):
    dicts={}
    if len(params)==0:
        return
    params = params.split('&')
    for param in params:
        dicts[param.split('=')[0]]=param.split('=')[1]
    return dicts
       
if __name__=='__main__':
    
    try:
        server = HTTPServer(('', 8000), MyRequestHandler)
        print('started httpserver...')
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()
    
    pass



"""
from wsgiref.simple_server import make_server


def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    para_path = environ['PATH_INFO']#[1:]  #PATH_INFO的第二位到最后一位（去掉"/"）
    para_val = (environ['QUERY_STRING'])
    if len(para_val.strip()) != 0:
        para_val = para_val.split('=')[1]
    return [(u"This is hello wsgi app : "+ para_path + " & " + para_val ).encode('utf8') ]

if __name__ == "__main__" :
    httpd = make_server('', 8000, simple_app)
    print("Serving on port 8000...")
    httpd.serve_forever()
""""""

"""
import socket
import sys
#import StringIO --in python 2.x
from io import StringIO

 
class WSGIServer(object):
 
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1
 
    def __init__(self, server_address):
        # Create a listening socket
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind
        listen_socket.bind(server_address)
        # Activate
        listen_socket.listen(self.request_queue_size)
        # Get server host name and port
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        # Return headers set by Web framework/Web application
        self.headers_set = []
 
    def set_app(self, application):
        self.application = application
 
    def serve_forever(self):
        listen_socket = self.listen_socket
        while True:
            # New client connection
            self.client_connection, client_address = listen_socket.accept()
            # Handle one request and close the client connection. Then
            # loop over to wait for another client connection
            self.handle_one_request()
 
    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024)
        # Print formatted request data a la 'curl -v'
        print(''.join(
            '&lt; {line}n'.format(line=line)
            for line in request_data.splitlines()
        ))
 
        self.parse_request(request_data)
 
        # Construct environment dictionary using request data
        env = self.get_environ()
 
        # It's time to call our application callable and get
        # back a result that will become HTTP response body
        result = self.application(env, self.start_response)
 
        # Construct a response and send it back to the client
        self.finish_response(result)
 
    def parse_request(self, text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('rn')
        # Break down the request line into components
        (self.request_method,  # GET
         self.path,            # /hello
         self.request_version  # HTTP/1.1
         ) = request_line.split()
 
    def get_environ(self):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = StringIO.StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = self.request_method    # GET
        env['PATH_INFO']         = self.path              # /hello
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        return env
 
    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response
 
    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}rn'.format(status=status)
            for header in response_headers:
                response += '{0}: {1}rn'.format(*header)
            response += 'rn'
            for data in result:
                response += data
            # Print formatted response data a la 'curl -v'
            print(''.join(
                '&gt; {line}n'.format(line=line)
                for line in response.splitlines()
            ))
            self.client_connection.sendall(response)
        finally:
            self.client_connection.close()
 
SERVER_ADDRESS = (HOST, PORT) = '', 8888
 
def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server
 
if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module,application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print('WSGIServer: Serving HTTP on port {port} ...n'.format(port=PORT))
    httpd.serve_forever()
"""

"""
from http.server import HTTPServer,BaseHTTPRequestHandler
import io,shutil

class MyHttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        r_str="Hello World"
        enc="UTF-8"
        encoded = ''.join(r_str).encode(enc)
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        shutil.copyfileobj(f,self.wfile)

        data = self.rfile.read(nbytes)
        write(data)

httpd=HTTPServer(('',8080),MyHttpHandler)
print("Server started on 127.0.0.1,port 8080.....")
httpd.serve_forever()
"""

"""

import socket
 
HOST, PORT = '', 8888
 
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...' % PORT)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print(request)
 
    http_response = "HTTP/1.1 200 OK"
    http_response += "\n Hello, World!"

    client_connection.sendall(http_response)
    client_connection.close()
"""
