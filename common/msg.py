#! /usr/bin/env python
# -*- coding: utf-8 -*-
list_cmd = ("propo", "joueur", "chat", "tick", 
    "askgrille", "asktour", "askscore", "asktirage", "askinfo",
    "connect", "error", "grille", "chrono", "mot_top", 
    "new", "tour", "score", "tirage", "valid", "info", "infojoueur",
    "next", "restart", "oknext", "okrestart", "stopchrono", "okstopchrono",
    "askall", "all",
    )

class msg :
    def __init__(self, cmd, param=None, id=None) :
        if cmd in list_cmd :
            self.cmd = cmd
        else :
            raise TypeError
        self.id = id
        self.param = param

    def __str__(self) :
        return " - ".join((self.cmd, repr(self.param), repr(self.id)))

    def set_id(self, id) :
        self.id = id
