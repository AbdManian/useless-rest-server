# Useless REST Server! 
#   Get last 10 requests (only GET/POST) to the server.
#   Formate: GET/POST | PATH | BODY | Time
#   Set server port by setting URS_PORT environment variable
# Based on https://blog.anvileight.com/posts/simple-python-http-server/

from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
import time
import os


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    log_list = []

    def store_log(self, method, path, body=b''):
        self.log_list.append(
            "{} | {} | {} | {}".format(
                method,
                path,
                body.decode('utf-8'),
                time.time()
            ))
        self.log_list = self.log_list[-10:]
    
    def get_logs(self):
        rstr = "\n".join(self.log_list)
        return rstr.encode('utf-8')

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.store_log('GET', self.path)
        self.wfile.write(self.get_logs())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        self.store_log('POST', self.path, body)
        self.wfile.write(self.get_logs())



port = int(os.getenv('URS_PORT', 8000))



print('<<<Useless REST Server>>>')
print('Start server port={}'.format(port))
httpd = HTTPServer(('', port), SimpleHTTPRequestHandler)
httpd.serve_forever()
