#! /usr/bin/env python
# -*- coding: utf-8 -*-

def lettre_joker(l) :
    if 'A' <= l <= 'Z' :
        return l
    elif 'a' <= l <= 'z' or l == '?' :
        return '?' 
    else :
        return ""

def convert_time(t) :
    try:
        t=int(t)
    except ValueError :
        return "00:00"

    if t>=0 :
        min = t//60
        sec = t-min*60
        return "%02d:%02d" % (min,sec)

def errordlg(msg, titre) :
    import wx 
    dlg = wx.MessageDialog(None,msg,titre,wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy() 

if __name__ == '__main__' :
    for i in range(180) :
        print convert_time(i)
