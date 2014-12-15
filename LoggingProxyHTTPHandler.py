import BaseHTTPServer
import gzip
import requests
import StringIO


def rewrite_headers(headers):
    # Don't accept stuff that original request didn't accept
    if not 'accept-encoding' in headers:
        headers['accept-encoding'] = 'identity'
    result = dict()
    for k, v in headers.items():
        newk = '-'.join(map(lambda x: x.capitalize(), k.split('-')))
        result[newk] = v
    return result

class LoggingProxyHTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    # send_response pretty similar to BaseHTTPServer send_response
    # but without Server or Date headers
    def send_response(self, code, message=None):
        self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            response = "{0} {1} {2}\r\n".format(self.protocol_version,
                                                code, message)
            self.wfile.write(response)

    def respond(self, response):
        if response.status_code < 400:
            self.send_response(response.status_code)
        else:
            self.send_error(response.status_code)
        for k, v in rewrite_headers(response.headers).items():
            self.send_header(k, v)
        self.end_headers()

        output = response.content
        # handle gzip
        # http://stackoverflow.com/questions/8506897/how-do-i-gzip-compress-a-string-in-python
        if 'content-encoding' in response.headers and \
                response.headers['content-encoding'].lower() == 'gzip':
            buffer = StringIO.StringIO()
            with gzip.GzipFile(fileobj=buffer, mode="w") as f:
                f.write(output)
            output = buffer.getvalue()

        # handle chunking
        # (thanks to https://gist.github.com/josiahcarlson/3250376)
        # although we only pretend to chunk and send it all at once!
        if 'transfer-encoding' in response.headers and \
                response.headers['transfer-encoding'].lower() == 'chunked':
            self.wfile.write('%X\r\n%s\r\n' %
                             (len(output), output))
            # send the chunked trailer
            self.wfile.write('0\r\n\r\n')
        else:
            self.wfile.write(output)
        self.log_response(response)

    def do_GET(self):
        headers = rewrite_headers(self.headers)
        response = requests.get(self.path, headers=headers)
        self.respond(response)

    def do_POST(self):
        headers = rewrite_headers(self.headers)
        self.data = self.rfile.read(int(self.headers['Content-Length']))
        response = requests.post(self.path, headers=headers, data=self.data)
        self.respond(response)

    def do_PUT(self):
        headers = rewrite_headers(self.headers)
        self.data = self.rfile.read(int(self.headers['Content-Length']))
        response = requests.put(self.path, headers=headers, data=self.data)
        self.respond(response)

    def log_error(format, *args):
        pass

    def log_request(self, *args):
        print "*** REQUEST ***"
        print self.command + ' ' + self.path
        for (k, v) in rewrite_headers(self.headers).items():
            print "{0} = {1}".format(k, v)
        print
        if self.command in ['POST', 'PUT']:
            print self.data
        print "*** END REQUEST ***"

    def log_response(self, response):
        print "*** RESPONSE ***"
        shortmessage, longmessage = self.responses[response.status_code]
        print "{0} {1}".format(response.status_code, shortmessage)
        for (k, v) in rewrite_headers(response.headers).items():
            print "{0} = {1}".format(k, v)
        print
        print response.content
        print "*** END RESPONSE ***"
