#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import yaml

class settings :
    def __init__(self) :
        nom = "settings.yaml"
        appname = "wxscrab"
        if sys.platform == 'win32':
            appdata = os.path.join(os.environ['APPDATA'], appname)
        else:
            appdata = os.path.expanduser(os.path.join("~", "." + appname))
        if not os.path.exists(appdata) :
            os.mkdir(appdata)
        self.file = os.path.join(appdata, nom)

        with open("def.yaml") as f :
            buff = f.read()
        self.dic = yaml.load(buff)
        self.def_keys = self.dic.keys()
        if os.path.isfile(self.file) :
            with open(self.file) as f :
                buff = f.read()
        dic_perso = yaml.load(buff)
        for key, item in dic_perso.iteritems() :
            self.dic[key] = item

    def write(self) :
        with open(self.file,"w") as f :
            dic = {}
            for key in self.def_keys :
                dic[key] = self.dic[key]
            f.write(yaml.dump(dic, default_flow_style=False))

    def set(self, key, val) :
        self.dic[key] = val

    def get(self, key) :
        return self.dic.get(key)

    def insert_list(self, key, val) :
        if val in self.dic[key] :
            self.dic[key].remove(val)
        self.dic[key].insert(0,val)

if __name__ == '__main__' :
    s = settings()
    print s.dic
