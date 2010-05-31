#! /usr/bin/env python
# -*- coding: utf-8 -*-
import xml.dom.minidom
import os
import sys

class settings :
    def __init__(self) :
        self.liste_skin = ("default", "tiny", "small", "big", "mega")
        self.liste_case = ("8","9","10")
        nom = "settings.xml"
        appname = "wxscrab"
        if sys.platform == 'win32':
            appdata = os.path.join(os.environ['APPDATA'], appname)
        else:
            appdata = os.path.expanduser(os.path.join("~", "." + appname))
        if not os.path.exists(appdata) :
            os.mkdir(appdata)
        self.file = os.path.join(appdata, nom)
        self.dic = {'servers' : ['wxscrab.ath.cx'],
                    'pseudo' : '',
                    'port' : '1989',
                    'email' : '',
                    'skin' : 'default',
                    'tirage_nbpos' : '8',
                    'policeserv' : '12',
                    'admin':False
                    }

        if os.path.isfile(self.file) :
            dom = xml.dom.minidom.parse(self.file)
            s = dom.getElementsByTagName("settings")[0]
            for n in s.childNodes:
                if n.nodeType != s.TEXT_NODE:
                    l = []
                    for o in n.childNodes :
                        if o.nodeType == s.TEXT_NODE:
                            self.dic[str(n.nodeName)] = str(o.data.strip())
                        else :
                            l.append(str(o.childNodes[0].data.strip()))
                    if l != [] :
                        self.dic[str(n.nodeName)] = l

    def write(self) :
        f = open(self.file,"w")
        doc = xml.dom.minidom.Document()
        top = doc.createElement("settings")
        doc.appendChild(top)
        for key,value in self.dic.iteritems() :
            elt = doc.createElement(key)
            if type(value) == str :
                text = doc.createTextNode(value)
                elt.appendChild(text)
            else :
                for val in value :
                    elt2 = doc.createElement("val")
                    text = doc.createTextNode(val)
                    elt2.appendChild(text)
                    elt.appendChild(elt2)
            top.appendChild(elt)
        doc.writexml(f,"","  ","\n")
        f.close()

    def set(self, key, val) :
        self.dic[key] = val

    def get(self, key) :
        return self.dic.get(key)

    def insert_list(self, key, val) :
        if val in self.dic[key] :
            self.dic[key].remove(val)
        self.dic[key].insert(0,val)
 
if __name__=='__main__' :
    s = settings()
    print s.dic
