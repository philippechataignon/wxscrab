#! /usr/bin/env python
# -*- coding: utf-8 -*-

import asyncore, asynchat
import socket 
import cPickle as pickle
import threading

class net (asyncore.dispatcher):
    def __init__(self, port, parent) :
        asyncore.dispatcher.__init__(self)
        self.parent = parent
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.actifs = []
        self.lock = threading.RLock()

    def handle_accept(self) :
        sock, addr = self.accept()
        if sock is not None :
            self.actifs.append(channel(sock, self))
            print "Connexion de %s" % repr(addr)
         
    def envoi_all(self, mm) :
        for c in self.actifs :
            c.envoi(mm) 

class channel(asynchat.async_chat) :
    term = "\r\n\r\n"
    def __init__(self, sock, server) :
        asynchat.async_chat.__init__(self, sock)
        self.server = server
        self.buffer = []
        self.set_terminator(channel.term)
        self.envoi_actif = True
        
    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self) :
        txt = "".join(self.buffer)
        self.buffer = []
        mm = pickle.loads(txt)
        if self.server.parent.options.verbose == True :
            print "<- %s" % mm.cmd
        self.server.parent.traite(self, mm)
        
    def handle_error(self) :
        print "handle_error"

    def handle_close(self) :
        self.server.actifs.remove(self)
        print "Deconnect %s" % repr(self)
        self.server.parent.deconnect(self)
        self.close()

    def envoi(self, mm):
        self.server.lock.acquire()
        if self.server.parent.options.verbose == True :
            print "-> %s" % mm.cmd
        self.push(pickle.dumps(mm) + channel.term)
        self.server.lock.release()
