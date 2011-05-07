#! /usr/bin/env python
# -*- coding: utf-8 -*-
list_cmd = ("propo", "joueur", "chat", "tick", 
    "askscore", "askinfo",
    "connect", "error", "chrono", "mot_top", 
    "new", "score", "tirage", "valid", "info", "infojoueur",
    "vote", "okvote",
    "askall", "all",
    )

class msg :
    def __init__(self, cmd, param=None, id=None) :
        if cmd in list_cmd :
            self.cmd = cmd
        else :
            raise TypeError(cmd)
        self.id = id
        self.param = param

    def __str__(self) :
        return " - ".join((self.cmd, repr(self.param), repr(self.id)))

    def set_id(self, id) :
        self.id = id
