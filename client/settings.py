#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import os
import sys
import yaml

class settings :
    def __init__(self) :
        nom = "settings.yaml"
        appname = "wxscrab"
        if sys.platform == 'win32':
            appdata = os.path.join(os.environ['APPDATA'], appname)
        else:
            appdata = os.path.expanduser(os.path.join("~", "." + appname))
        if not os.path.exists(appdata) :
            os.mkdir(appdata)
        self.file = os.path.join(appdata, nom)

        with open("def.yaml") as f :
            buff = f.read()
        if os.path.isfile(self.file) :
            with open(self.file) as f :
                buff += f.read()
        self.dic = yaml.load(buff)
        self.img = {}
        dir = self.get('files','rep_images')
        size = self.get('size', 'size')
        for key, nom in self.dic['images'].items() :
            img = wx.Image(os.path.join(dir, nom) ,wx.BITMAP_TYPE_PNG).Scale(size,size)
            if key == 'fl_r' :
                self.img[key] = wx.BitmapFromImage(img.Rotate90(False))
            else :
                self.img[key] = wx.BitmapFromImage(img)
        self.font_norm = wx.Font(self.get('size', 'fontsize'),wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False,"")
        self.font_point = wx.Font(self.get('size', 'pointfontsize'),wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False,"")

    def write(self) :
        with open(self.file,"w") as f :
            f.write(yaml.dump(self.dic, default_flow_style=False))

    def set(self, chap, key, val) :
        self.dic[chap][key] = val

    def get(self, chap, key) :
        return self.dic.get(chap).get(key)

    def insert_list(self, chap, key, val) :
        if val in self.dic[chap][key] :
            self.dic[chap][key].remove(val)
        self.dic[chap][key].insert(0,val)
 
    def get_img(self, nom) :
        return self.img[nom]

    def get_img_copy(self, nom) :
        bmp_org =  self.img[nom]
        bmp =  bmp_org.GetSubBitmap(wx.Rect(0, 0, bmp_org.GetWidth(), bmp_org.GetHeight()))
        return bmp

    def get_font(self) :
        return self.font_norm

    def get_pointfont(self) :
        return self.font_point

if __name__ == '__main__' :
    import yaml
    print yaml.dump(s.param, default_flow_style=False)
    print yaml.dump(s.fontcol,default_flow_style=False)

