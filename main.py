#!/usr/bin/python
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from utils import ElementStruct, ParsedPath, Utils

PORT_NUMBER = 4443

root_elements = []
elements = []


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        self.end_headers()

        parsed_path = Utils.parse_path(self.path)
        if parsed_path.root == "/":
            self.get_root_elements()
        elif parsed_path.field_name == "":
            if parsed_path.root != "" and parsed_path.device_name == "":
                self.get_elements_by_root(parsed_path.root, False)
            elif parsed_path.root != "" and parsed_path.device_name != "":
                self.get_fields_by_element(parsed_path.device_name, False)
        elif parsed_path.field_name != "":
            self.get_field_by_name(parsed_path.field_name, parsed_path)

        return

    # def do_POST(self):
    #     content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
    #     post_data = self.rfile.read(content_length)
    #
    #     print json.loads(post_data)
    #
    #     self.send_response(200)
    #     # self.send_header('Content-type', 'text/html')
    #     self.end_headers()

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

    def get_field_by_name(self, field_name, parsed_path):
        for r in root_elements:
            if r.name == parsed_path.root:
                for el in elements:
                    if r.name == el.root and el.name == parsed_path.device_name:
                        if field_name in el.values:
                            self.wfile.write(el.values[field_name])

if __name__ == "__main__":

    root_elements.append(ElementStruct("/", "devices", ""))
    root_elements.append(ElementStruct("/", "test_field", ""))

    elements.append(ElementStruct("devices", "wifi_1", {"on": 123, "off": 28}))
    elements.append(ElementStruct("devices", "wifi_2", {"one": "fuck", "second": 56}))
    elements.append(ElementStruct("devices", "wifi_3", {"third": "789"}))

    elements.append(ElementStruct("test_field", "wifi"))

    try:
        server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
        print "Started http server on port:\t" + str(PORT_NUMBER)

        # wait for request
        server.serve_forever()

    except KeyboardInterrupt:
        print "Server was interrupt"
        server.socket.close()
