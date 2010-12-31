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
        self.dic = yaml.load(buff)
        self.def_keys = self.dic.keys()
        self.def_keys.remove('images')
        if os.path.isfile(self.file) :
            with open(self.file) as f :
                buff = f.read()
        dic_perso = yaml.load(buff)
        for key, item in dic_perso.iteritems() :
            self.dic[key] = item
        self.img = {}
        size = self.get('size_jeton')
        self.calc_auto()
        dir = self.get('files_rep_images')
        for key, nom in self.dic['images'].items() :
            img = wx.Image(os.path.join(dir, nom) ,wx.BITMAP_TYPE_PNG).Scale(size,size)
            if key == 'fl_r' :
                self.img[key] = wx.BitmapFromImage(img.Rotate90(False))
            else :
                self.img[key] = wx.BitmapFromImage(img)
        self.font_norm = wx.Font(self.get('size_font_jeton'),wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False,"")
        self.font_point = wx.Font(self.get('size_font_point'),wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False,"")

    def calc_auto(self) :
        size = self.get('size_jeton')
        self.dic['size_offset_coord'] = (size * 2) / 3
        self.dic['size_font_jeton'] = size / 2
        self.dic['size_font_point'] = (size * 15) / 100
        self.dic['size_font_chrono'] = size / 2
        self.dic['size_font_score'] = (4*size)/10
        self.dic['size_fill'] = size/2

    def write(self) :
        with open(self.file,"w") as f :
            dic = {}
            for key in self.def_keys :
                dic[key] = self.dic[key]
            f.write(yaml.dump(dic, default_flow_style=False))

    def set(self, key, val) :
        self.dic[key] = val

    def get(self, key) :
        return self.dic.get(key)

    def insert_list(self, key, val) :
        if val in self.dic[key] :
            self.dic[key].remove(val)
        self.dic[key].insert(0,val)
 
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
