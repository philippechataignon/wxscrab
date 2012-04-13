#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json

list_cmd = (
    "all",
    "askall",
    "askinfo",
    "askscore",
    "chat",
    "chrono",
    "connect",
    "error",
    "info",
    "infojoueur",
    "joueur",
    "mot_top",
    "new",
    "okvote",
    "propo",
    "score",
    "serverok",
    "tick",
    "tirage",
    "valid",
    "vote",
)

class msg :
    def __init__(self, cmd = None, param=None, nick=None, dump=None) :
        if dump is None :
            self.cmd = cmd
            self.nick = nick
            self.param = param
        else :
            self.cmd, self.param, self.nick = json.loads(dump)
        if self.cmd not in list_cmd :
            print "Erreur : commande %s" % self.cmd
            self.cmd = None

    def __str__(self) :
        return repr([self.cmd, self.param, self.nick])

    def set_nick(self, nick) :
        self.nick = nick

    def dump(self) :
        return json.dumps([self.cmd, self.param, self.nick])

if __name__ == '__main__' :
    m = msg("chat", [0, 2], "philippe")
    d = m.dump()
    print m, d
    n = msg(dump=d)
    print n, d
    m = msg("chat")
    print m, m.dump()
