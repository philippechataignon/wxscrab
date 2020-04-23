#!/usr/bin/env python3
import json
import urllib.request

class Dico:
    def __init__(self, nom_dico):
        pass

    def isMot(self, mot):
        contents = urllib.request.urlopen(f"http://localhost:1964/is_mot/{mot}").read()
        ret = json.loads(contents)
        return ret["ok"]

if __name__ == '__main__':
    d = Dico("ods8")
    print(d.isMot("pipo"))
    print(d.isMot("pipon"))
