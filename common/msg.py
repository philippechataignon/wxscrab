#! /usr/bin/env python
# -*- coding: utf-8 -*-
import yaml

list_cmd = ("propo", "joueur", "chat", "tick", 
    "askscore", "askinfo",
    "connect", "error", "chrono", "mot_top", 
    "new", "score", "tirage", "valid", "info", "infojoueur",
    "vote", "okvote",
    "askall", "all",
    )

class msg :
    def __init__(self, cmd = None, param=None, id=None, dump=None) :
        if dump is None :
            if cmd in list_cmd :
                self.cmd = cmd
            else :
                raise TypeError(cmd)
            self.id = id
            self.param = param
        else :
            self.cmd, self.param, self.id = yaml.load(dump)

    def __str__(self) :
        return " - ".join((self.cmd, repr(self.param), repr(self.id)))

    def set_id(self, id) :
        self.id = id

    def dump(self) :
        return yaml.dump([self.cmd, self.param, self.id])

if __name__ == '__main__' :
    m = msg("chat", [0, 2], "philippe")
    print m
    d = m.dump()

    n = msg(dump=d)
    print n

    
    m = msg("chat")
    print m, m.dump()
