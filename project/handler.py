import socketserver


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print(f"Received {self.data} from {self.client_address[0]}")
        self.request.sendall(self.data)
