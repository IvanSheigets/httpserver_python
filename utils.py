class ParsedPath(object):
    service = ""
    resource = ""
    field_name = ""

    def __init__(self, service="", resource="", field=""):
        self.service = service
        self.resource = resource
        self.field_name = field


class ElementStruct(object):
    root = ""
    name = ""
    values = {}

    def __init__(self, root="", name="", values={}):
        self.root = root
        self.name = name
        self.values = values


class Utils(object):
    @staticmethod
    def parse_path(path):
        parsed_path = ParsedPath()
        if path == "/":
            parsed_path.service = "/"
        else:
            pos = path.find('?')
            if pos != -1:
                parsed_path.field_name = path[pos + 1:]
                path = path[0:pos]

            path = path.strip("/").split("/")

            l = len(path)
            if l == 1:
                parsed_path.service = path[0]
            elif l == 2:
                parsed_path.service = path[0]
                parsed_path.resource = path[1]

        return parsed_path

    @staticmethod
    def is_element_present(services, resources, parsed_path):
        is_present = False
        for res in resources:
            if res.name == parsed_path.device_name:
                for ser in services:
                    if res.root == ser.name and parsed_path.root == ser.name:
                        is_present = True
        return is_present

    # @staticmethod
    # def is_
