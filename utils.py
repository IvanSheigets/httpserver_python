class ParsedPath(object):
    root = ""
    device_name = ""
    field_name = ""

    def __init__(self, root="", name="", field=""):
        self.root = root
        self.device_name = name
        self.field_name = field


class ElementStruct(object):
    root = ""
    name = ""
    values = {}

    def __init__(self, root, name, values={}):
        self.root = root
        self.name = name
        self.values = values


class Utils(object):
    @staticmethod
    def parse_path(path):
        parsed_path = ParsedPath()
        if path == "/":
            parsed_path.root = "/"
        else:
            pos = path.find('?')
            if pos != -1:
                parsed_path.field_name = path[pos + 1:]
                path = path[0:pos]

            path = path.strip("/").split("/")

            l = len(path)
            if l == 1:
                parsed_path.root = path[0]
            elif l == 2:
                parsed_path.root = path[0]
                parsed_path.device_name = path[1]

        return parsed_path
