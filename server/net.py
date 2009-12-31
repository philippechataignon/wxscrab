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

    def handle_accept(self) :
        sock, addr = self.accept()
        if sock is not None :
            channel(sock, self)
            print "Connexion de %s" % repr(addr)
         
    def envoi_all(self, mm) :
        for c in asyncore.socket_map.values() :
            try :
                c.envoi(mm) 
            except AttributeError :
                pass

class channel(asynchat.async_chat) :
    term = "\r\n\r\n"
    def __init__(self, sock, server) :
        asynchat.async_chat.__init__(self, sock)
        self.server = server
        self.buffer = []
        self.set_terminator(channel.term)
        self.lock = threading.Lock()
        
    def collect_incoming_data(self, data):
        self.lock.acquire()
        self.buffer.append(data)
        self.lock.release()

    def found_terminator(self) :
        self.lock.acquire()
        txt = "".join(self.buffer)
        self.buffer = []
        self.lock.release()
        try:
            mm = pickle.loads(txt)
            if self.server.parent.options.verbose == True :
                print "<- %s" % mm.cmd
            self.server.parent.traite(self, mm)
        except pickle.PicklingError:
            pass

    def handle_close(self) :
        print "Deconnect %s" % repr(self)
        self.server.parent.deconnect(self)
        self.close()

    def envoi(self, mm):
        self.lock.acquire()
        if self.server.parent.options.verbose == True :
            print "-> %s" % mm.cmd
        self.push(pickle.dumps(mm) + channel.term)
        self.lock.release()
