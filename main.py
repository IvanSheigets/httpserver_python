#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT_NUMBER = 4443

root_elements = []
elements = []


class ElememntStruct(object):
    root = ""
    name = ""
    values = {}

    def __init__(self, root, name, values={}):
        self.root = root
        self.name = name
        self.values = values


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        self.end_headers()

        path = self.path.strip('/')

        if path == "":
            self.get_root_elements()
        elif path.find('?') == -1:
            path = path.split("/")
            if len(path) == 1:
                self.get_elements_by_root(path[0], False)
            elif len(path) == 2:
                self.get_fields_by_element(path[1], False)
        else:
            pos = path.find('?')
            if pos != -1:
                element_name = path[pos + 1:]
                path = path[0:pos]
                path = path.split("/")
                if len(path) >= 2:
                    self.get_field_by_name(element_name, path)

        return

    def get_root_elements(self):
        for r in root_elements:
            self.wfile.write(r.name + "\n")
            # get elements contains in root
            self.get_elements_by_root(r.name)
            self.wfile.write("\n")

    def get_elements_by_root(self, root_name, shift=True):
        for el in elements:
            if el.root == root_name:
                self.wfile.write(("\t" if shift else "") + el.name + "\n")
                self.get_fields_by_element(el.name)

    def get_fields_by_element(self, element_name, shift=True):
        for el in elements:
            if el.name == element_name:
                for name, value in el.values.items():
                    self.wfile.write(("\t\t" if shift else "") + str(name) + " : " + str(value) + "\n")

    def get_field_by_name(self, field_name, path=[]):
        for r in root_elements:
            if r.name == path[0]:
                for el in elements:
                    if r.name == el.root and el.name == path[1]:
                        if field_name in el.values:
                            self.wfile.write(el.values[field_name])

if __name__ == "__main__":

    root_elements.append(ElememntStruct("/", "devices", ""))
    root_elements.append(ElememntStruct("/", "test_field", ""))

    elements.append(ElememntStruct("devices", "wifi_1", {"on": 123, "off": 28}))
    elements.append(ElememntStruct("devices", "wifi_2", {"one": "fuck", "second": 56}))
    elements.append(ElememntStruct("devices", "wifi_3", {"third": "789"}))

    elements.append(ElememntStruct("test_field", "wifi"))

    try:
        server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
        print "Started http server on port:\t" + str(PORT_NUMBER)

        # wait for request
        server.serve_forever()

    except KeyboardInterrupt:
        print "Server was interrupt"
        server.socket.close()
