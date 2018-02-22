#!/usr/bin/python


root_elements = ["devices", "test_field"]

elementList = []


class ElememntStruct(object):
    root = ""
    name = ""
    value = ""

    def __init__(self, root, name, value):
        self.root = root
        self.name = name
        self.value = value


if __name__ == "__main__":

    s = "/devices"
    # print s.lstrip("/")
    # print s[s.find('/')+1: s.find('/', 1)]
    s = s.lstrip('/')
    pos = s.find('/')
    if pos != -1:
        print s[0, pos]
    else:
        print s
