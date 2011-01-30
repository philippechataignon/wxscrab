#! /usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import wx.grid
import xml.etree.ElementTree as ET
from xml.parsers.expat import ExpatError

class CustomDataTable(wx.grid.PyGridTableBase):
    def __init__(self, tree):
        wx.grid.PyGridTableBase.__init__(self)
        self.colLabels = []
        self.rowLabels = []
        self.data = []
        self.max_len_row = 0
        for n in tree.findall('label/col') :
            self.colLabels.append(n.text)

        for l in tree.findall('ligne') :
            n = l.find('nom')
            self.rowLabels.append(n.text)
            if len(n.text) > self.max_len_row :
                self.max_len_row = len(n.text)
            cur_row_data = []
            for c in l.findall('val') :
                type = c.attrib.get('type')
                if type == 'i' :
                    v = int(c.text)
                elif type == 'f' :
                    v = float(c.text)
                else :
                    v = c.text
                cur_row_data.append(v)
            self.data.append(cur_row_data)

    def sort(self, col, rev) :
        z=zip(self.rowLabels, self.data)
        if col == 0 :
            z.sort(key=lambda x: x[0], reverse=rev)
        else :
            z.sort(key=lambda x: x[1][col-1], reverse=rev)
        self.rowLabels = [x[0] for x in z]
        self.data = [x[1] for x in z]

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.colLabels)

    def IsEmptyCell(self, row, col):
        return not self.data[row][col]

    def GetValue(self, row, col):
        return self.data[row][col]

    def SetValue(self, row, col, value):
        self.data[row][col] = value

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetRowLabelValue(self,row):
        return self.rowLabels[row]

class ScoreGrid(wx.grid.Grid):
    def __init__(self, parent, tree):
        wx.grid.Grid.__init__(self, parent, -1)
        self.table = CustomDataTable(tree)
        self.SetTable(self.table, True)
        self.EnableEditing(False)
        self.EnableDragGridSize(False)
        self.EnableDragColSize(False)
        self.EnableDragRowSize(False)
        self.AutoSizeColumns()
        self.SetRowLabelSize(self.table.max_len_row * self.GetLabelFont().GetPointSize())
        self.SetDefaultCellAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        self.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        self.SetSize(self.GetBestSize())
        self.SetScrollbars(0,0,0,0,0,0)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnClick)
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.OnClick)
        self.col_tri = 0
        self.rev = True
        self.tri(1)
    
    def OnClick(self,e) :
        c = e.GetCol()+1
        self.tri(c)

    def tri(self, c) :
        # on reclique sur la colonne du tri actuel
        if self.col_tri == c :
            self.rev = not self.rev
        else :
            self.col_tri = c
            self.rev = True
        self.table.sort(self.col_tri, self.rev)
        self.Refresh()
            
class frame_score(wx.Frame):
    def __init__(self, parent, data = None) :
        wx.Frame.__init__(self, parent, -1, "wxScrab scores", style=wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.CAPTION)
        panel = wx.Panel(self, -1)
        border = wx.BoxSizer(wx.VERTICAL)
        # data est None à la création initiale dans wxscrab
        if data is not None :
            try :
                tree = ET.XML(data)
            # si on ne peut pas parser le XML => frame vide mais pas d'erreur
            except (SyntaxError, ExpatError) :
                pass
            else :
            # on passe le tree pour constituer la table de données
                grid = ScoreGrid(panel, tree)
                border.Add(grid, 0, wx.ALL, 10)
        butt = wx.Button(panel, 10, "Fermer")
        border.Add(butt, 0, wx.ALL|wx.ALIGN_RIGHT, 10)
        self.Bind(wx.EVT_BUTTON, self.quit, butt)
        self.Bind(wx.EVT_CLOSE, self.quit)
        panel.SetSizerAndFit(border)
        self.SetSize(self.GetBestSize())
        self.Centre()
 
    def quit(self,evt) :
        self.Hide()

if __name__ == '__main__' :
    #Pas tres propre mais c'est pour tester
    class App(wx.App):
        def OnInit(self) :
            t="""<score>
            <label>
            <col>Total</col><col>%</col></label>
            <ligne><nom>Xouillet</nom><val>250</val><val type="f">24.325</val></ligne>
            <ligne><nom>mlerose</nom><val>750</val><val type="i">86</val></ligne>
            <ligne><nom>Kikoolol</nom><val>210</val><val type="f">23</val></ligne>
            <ligne><nom>Bibilolo</nom><val>430</val><val>30</val></ligne></score>
            """
            self.score = frame_score(None, t) 
            self.score.Show()
            return True
    app = App()
    app.MainLoop()
