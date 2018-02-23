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

    s = "/devices/wifi?hello"
    pos = s.find('?')
    el = s[pos+1:]
    s = s[0:pos]
    s = s.strip('/').split('/')
    last = s[len(s)-1]

    print el
    print last[last.find('?')+1:]
    print s
