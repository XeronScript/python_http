from http.server import BaseHTTPRequestHandler, HTTPServer


class EchoHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, headers=None):
        self.send_response(status_code)
        if headers:
            for key, value in headers.items():
                self.send_header(key, value)
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write(self.path.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(content_length)

        self._set_response()
        self.wfile.write(request_data)


def run(server=HTTPServer, handler=EchoHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server(server_address, handler)
    print(f'Starting echo HTTP server on port {port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
