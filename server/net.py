#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import asyncore, asynchat
import socket 
import cPickle as pickle
import threading

class net (asyncore.dispatcher):
    def __init__(self, parent) :
        asyncore.dispatcher.__init__(self)
        self.parent = parent
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', self.parent.options.port))
        self.listen(5)
        self.lock = threading.RLock()

    def handle_accept(self) :
        sock, addr = self.accept()
        if sock is not None :
            channel(sock, self)
            print "Connexion de %s" % repr(addr)
         
class channel(asynchat.async_chat) :
    term = "\r\n\r\n"
    def __init__(self, sock, server) :
        asynchat.async_chat.__init__(self, sock)
        self.server = server
        self.buffer = []
        self.set_terminator(channel.term)
        
    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self) :
        txt = "".join(self.buffer)
        self.buffer = []
        mm = pickle.loads(txt)
        if self.server.parent.options.verbose == True :
            print "<- %s" % mm
        self.server.parent.traite(self, mm)
        
    def handle_close(self) :
        print "Deconnect %s" % repr(self)
        self.server.parent.deconnect(self)
        self.close()

    def envoi(self, mm):
        if self.server.parent.options.verbose == True :
            print "-> %s" % mm
        msg = pickle.dumps(mm, pickle.HIGHEST_PROTOCOL) + channel.term
        self.server.lock.acquire()
        self.push(msg)
        self.server.lock.release()
