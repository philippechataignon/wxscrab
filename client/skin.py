#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import wx
import sys

if sys.version[:3]>='2.5' :
    import xml.etree.ElementTree as ET
else :
    import elementtree.ElementTree as ET

class skin :
    def __init__(self, nom) :
        dir = 'skins'
        file  = os.path.join(dir, nom + '.xml')
        tree = ET.ElementTree(file=file)
        elem = tree.getroot()
        self.param = {}
        self.fontcol= {}

        for node in elem :
            if node.tag == "fontcol" :
                self.fontcol[node.attrib["name"]] = node.text
            else :
                try :
                    self.param[node.tag] = int(node.text)
                except ValueError :
                    self.param[node.tag] = node.text

        dir_images='images'
        dir = os.path.join(dir_images, self.param['rep_images'])
        size = self.param['size']
        nom_img = {
            'null':"tile_null.png", 
            'ld'  :"tile_DL.png",   
            'lt'  :"tile_TL.png",   
            'md'  :"tile_DW.png",   
            'mt'  :"tile_TW.png",   
            'temp':"tile_blanc.png",
            'norm':"tile.png",      
            'vide':"tile_vide.png", 
            'fl_b':"fleche_bas.png",
            'fl_r':"fleche_bas.png",
        }
        self.img = {}
        for key, nom in nom_img.items() :
            img = wx.Image(os.path.join(dir,nom) ,wx.BITMAP_TYPE_PNG).Scale(size,size)
            if key == 'fl_r' :
                self.img[key] = wx.BitmapFromImage(img.Rotate90(False))
            else :
                self.img[key] = wx.BitmapFromImage(img)
        self.font_norm = wx.Font(self.get('fontsize'),wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False,"")
        self.font_point = wx.Font(self.get('pointfontsize'),wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_BOLD,False,"")

    def get(self, nom) :
        return self.param[nom]

    def get_fontcol(self, nom) :
        return self.fontcol[nom]

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
