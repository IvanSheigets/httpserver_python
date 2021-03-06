#!/usr/bin/python
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from utils import ElementStruct, ParsedPath, Utils, MyElement

PORT_NUMBER = 4443

services = []
resources = []


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        self.end_headers()

        counter = 1
        data = {}
        for s in services:
            print "---> ELEMENT #" + str(counter)
            print s.id
            print s.major
            print s.minor
            print s.data
            print ""

            data["id"] = str(s.id)
            data["major"] = str(s.major)
            data["minor"] = str(s.minor)
            data["data"] = str(s.data)
            json_data = json.dumps(data)
            print json_data
            self.wfile.write(json_data)
            self.wfile.write("\n")
            counter += 1

        # parsed_path = Utils.parse_path(self.path)
        # if parsed_path.service == "/":
        #     self.get_root_elements()
        #
        # elif parsed_path.field_name == "":
        #     if parsed_path.service != "" and parsed_path.resource == "":
        #         self.get_elements_by_service_name(parsed_path.service, False)
        #     elif parsed_path.service != "" and parsed_path.resource != "":
        #         self.get_fields_by_resource_name(parsed_path.resource, False)
        # elif parsed_path.field_name != "":
        #     self.get_field_by_name(parsed_path.field_name, parsed_path)

        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)
        print "***********JSON**********"
        print post_data
        print "***********END_JSON**********"

        data = json.loads(post_data)
        if "sensor" in data:
            element = MyElement()
            element.id = int(data["sensor"]["id"])
            element.major = int(data["sensor"]["major"])
            element.minor = int(data["sensor"]["minor"])
            element.data = float(data["sensor"]["data"])
            services.append(element)


        # parsed_path = Utils.parse_path(self.path)
        # if parsed_path.root == "/":
        #     element = ElementStruct()
        #     data = json.loads(post_data)
        #     if "name" in data:
        #         element.root = "/"
        #         element.name = data["name"]
        #         element.values = {"123"}
        #         services.append(element)
        #
        # print '\n'.join(str(p.root) + str(p.name) + str(p.values) for p in services)


        self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        self.end_headers()

    def get_root_elements(self):
        for r in services:
            self.wfile.write(r.name + "\n")
            # get elements contains in root
            self.get_elements_by_service_name(r.name)
            self.wfile.write("\n")

    def get_elements_by_service_name(self, service_name, shift=True):
        for el in resources:
            if el.root == service_name:
                self.wfile.write(("\t" if shift else "") + el.name + "\n")
                self.get_fields_by_resource_name(el.name)

    def get_fields_by_resource_name(self, resource_name, shift=True):
        for el in resources:
            if el.name == resource_name:
                for name, value in el.values.items():
                    self.wfile.write(("\t\t" if shift else "") + str(name) + " : " + str(value) + "\n")

    def get_field_by_name(self, field_name, parsed_path):
        for r in services:
            if r.name == parsed_path.service:
                for el in resources:
                    if r.name == el.root and el.name == parsed_path.resource:
                        if field_name in el.values:
                            self.wfile.write(el.values[field_name])




if __name__ == "__main__":

    services.append(MyElement(1, 1, 1, 20.3))

    # services.append(ElementStruct("/", "devices", ""))
    # services.append(ElementStruct("/", "test_field", ""))
    #
    # resources.append(ElementStruct("devices", "wifi_1", {"on": 123, "off": 28, "ivan": 40}))
    # resources.append(ElementStruct("devices", "wifi_2", {"one": "fuck", "second": 56}))
    # resources.append(ElementStruct("devices", "wifi_3", {"third": "789"}))
    #
    # resources.append(ElementStruct("test_field", "wifi"))

    try:
        server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
        print "Started http server on port:\t" + str(PORT_NUMBER)

        # wait for request
        server.serve_forever()

    except KeyboardInterrupt:
        print "Server was interrupt"
        server.socket.close()
