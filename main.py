#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 4443

element_list = {"car": "opel", "color": "black"}


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        element = str(self.path)
        element = element.lstrip('/')
        if element in element_list:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Send the html message
            self.wfile.write(element_list[element])
        else:
            self.send_response(404)

        return


if __name__ == "__main__":

    try:
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print "Started http server on port:\t" + str(PORT_NUMBER)

        # wait for request
        server.serve_forever()

    except KeyboardInterrupt:
        print "Server was interrupt"
        server.socket.close()
