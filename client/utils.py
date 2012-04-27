# -*- coding: utf-8 -*-

def convert_time(t) :
    try:
        t=int(t)
    except ValueError :
        return "00:00"

    if t>=0 :
        return "%02d:%02d" % (t // 60, t % 60)

def errordlg(msg, titre) :
    import wx 
    dlg = wx.MessageDialog(None,msg,titre,wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy() 

if __name__ == '__main__' :
    for i in range(180) :
        print convert_time(i)
