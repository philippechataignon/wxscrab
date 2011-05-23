#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json

list_cmd = ("propo", "joueur", "chat", "tick", 
    "askscore", "askinfo",
    "connect", "error", "chrono", "mot_top", 
    "new", "score", "tirage", "valid", "info", "infojoueur",
    "vote", "okvote",
    "askall", "all",
    "serverok",
    )

class msg :
    def __init__(self, cmd = None, param=None, nick=None, dump=None) :
        if dump is None :
            #assert cmd in list_cmd, "Msg cmd hors liste"
            self.cmd = cmd
            self.nick = nick
            self.param = param
        else :
            self.cmd, self.param, self.nick = json.loads(dump)

    def __str__(self) :
        return " - ".join((self.cmd, repr(self.param), repr(self.nick)))

    def set_nick(self, nick) :
        self.nick = nick

    def dump(self) :
        return json.dumps([self.cmd, self.param, self.nick])

if __name__ == '__main__' :
    m = msg("chat", [0, 2], "philippe")
    print m
    d = m.dump()

    n = msg(dump=d)
    print n

    
    m = msg("chat")
    print m, m.dump()
