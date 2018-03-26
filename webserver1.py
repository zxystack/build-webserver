# *-* coding: utf-8 *-* 

import socket 


HOST, PORT = 'localhost', 8080
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.bind((HOST, PORT))
listen_socket.listen(20)
while 1:
    connection, address = listen_socket.accept()
    request = connection.recv(1024)
    line = request.splitlines()
    line = line[0].strip('\r\n')
    print line 
    http_response = """\
HTTP/1.1 200 OK  

    Hello, World! 
                    """
    connection.sendall(http_response) 
    connection.close()  




import socket 

class WSGIServer(object):
    address_family = socket.AF_INET 
    socket_type = socket.SOCK_STREAM 
    request_queue_size = 5

    def __init__(self, address):
        self.socket = socket.socket(self.address_family, self.socket_type)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(address)
        self.socket.listen(self.request_queue_size)
        self.host, self.port = self.socket.getsockname()
        self.server_name = socket.getfqdn(self.host)

    def set_app(self, application):
        self.application = application 

    def server_forever(self):
        while 1:
            self.connection, client_address = self.socket.accept()
            self.request_handler(self.connection)

    def request_handelr(self):
        self.request_data = self.connection.recv(1024)
        self.parse_request()
        env = self.get_env()
        result = self.application(env, self.start_response)
        self.finish_response(result)

    def parse_request(self):
        request_data = request_data.splitlines()
        request_line = request_data.strip('\r\n')[0]
        self.request_method, self.request_path, self.request_version = request_line.split()

    def get_env(self):
        env = {}
        # WSGI必要参数
        env['wsgi.version']      = (1, 0) 
        env['wsgi.url_scheme']   = 'http' 
        env['wsgi.input']        = StringIO.StringIO(self.request_data) #返回一个
        env['wsgi.errors']       = sys.stderr 
        env['wsgi.multithread']  = False 
        env['wsgi.multiprocess'] = False 
        env['wsgi.run_once']     = False 
        ### CGI 必需变量 
        env['REQUEST_METHOD']    = self.request_method    # GET 
        env['PATH_INFO']         = self.path              # /hello 
        env['SERVER_NAME']       = self.server_name       # localhost 
        env['SERVER_PORT']       = str(self.server_port)  # 8888 
        return env

    def start_response(status. response_headers):
        '''
            this function is used to set response_headers and status 
        ''' 
        self.headers = [status, response_headers]

    def finish_response(self, result):
        try:
            status, headers = self.headers 
            reponse = 'HTTP/1.1 {status}\r\n'
            for h in headers:
                response += '{0}:{1}'.format(*h)
            response += '\r\n'
            for data in result:
                reponse += data 
            self.connection.sendall(response)
        finally:
            self.connection.close()

ADDRESS = ('localhost', 8888)
if __name__ == '__main__':
    import sys 
    if len(sys.args) < 2:
        return 'must give module:callable'
    app_path = sys.args[1]
    path, app = app_path.split(':')
    module = __import__(path)
    app = getattr(moudle, app)
    server = WSGIServer(ADDRESS)
    server.set_app(app)
    server.server_forever()