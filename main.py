#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 4443

root_elements = []
elements = []


class ElememntStruct(object):
    root = ""
    name = ""
    value = ""

    def __init__(self, root, name, value):
        self.root = root
        self.name = name
        self.value = value


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        self.end_headers()

        path = self.path

        # TODO /devices/ it trims last character
        if path == "/":
            self.get_root_elements()
        elif path.lstrip('/') != "":
            dev = path[path.find('/') + 1:path.find('/', 1)]
            self.get_element_by_root(dev)

        return

    def get_root_elements(self):
        for r in root_elements:
            self.wfile.write(r.name + "\n")
            for el in elements:
                if el.root == r.name:
                    self.wfile.write("\t" + str(el.name) + "\n")
            self.wfile.write("\n")

    def get_element_by_root(self, dev):
        for el in elements:
            print el.root
            if el.root == dev:
                self.wfile.write(el.name + "\n")


if __name__ == "__main__":

    root_elements.append(ElememntStruct("/", "devices", ""))
    root_elements.append(ElememntStruct("/", "test_field", ""))

    elements.append(ElememntStruct("devices", "wifi_1", "on"))
    elements.append(ElememntStruct("devices", "wifi_2", "on"))
    elements.append(ElememntStruct("devices", "wifi_2", "on"))

    elements.append(ElememntStruct("test_field", "wifi", "on"))

    try:
        server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
        print "Started http server on port:\t" + str(PORT_NUMBER)

        # wait for request
        server.serve_forever()

    except KeyboardInterrupt:
        print "Server was interrupt"
        server.socket.close()
