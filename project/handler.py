
import socketserver
import project.common

class RequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = project.common.recv_all(self.request).decode()
        httpRequest = self.data.split('\r\n')
        requestInfo = httpRequest[0].split(' ')
        method = requestInfo[0]
        endpoint = requestInfo[1]
        #print(httpRequest)
        print(method + ' ' + endpoint)
        self.request.sendall(self.data)
