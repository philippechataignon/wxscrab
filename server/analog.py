#!/usr/bin/env python2

import sys
import xml.etree.cElementTree as ET

tree = ET.ElementTree(file=sys.argv[1])
elem = tree.getroot()
tab=[]
nom_top='##TOP##'
liste_nick=[nom_top]
for tour in tree.findall("tour") :
    num=int(tour.attrib['num'])
    dic={}
    for prop in tour.findall("top") :
        dic[nom_top]=( prop.find("coord").text,  prop.find("mot").text,  int(prop.find("score").text))
    for prop in tour.findall("prop") :
        nick = prop.find("nick").text
        if nick not in liste_nick :
            liste_nick.append(nick)
        dic[nick]=(prop.find("coord").text,  prop.find("mot").text,  int(prop.find("score").text))
    tab.append(dic)
cum = {}
liste_nick.sort()

print("""\
<html>
<head>
<style type="text/css">
th  {text-align:center; border-bottom: 1px solid; border-left: 1px solid}
td  {text-align:right;border-left: 1px dashed; }
td.l  {text-align:left;border-left: 1px dashed; }
.extr  {text-align:center;border-left: 1px solid;}
</style>
</head>
<body>
""")
print("""\
<table style="border: 1px solid" cellpadding="2">
  <tr>
  <th>Tour</th>
""")
for nick in liste_nick :
    cum[nick] = 0 
    print("""<th colspan="5">%s</th>""" % nick)
print("""\
  </tr>
  <tr>
  <td>&nbsp;</td>
""")
for nick in liste_nick :
    print("<th>Coord</th> <th>Mot</th> <th>Score</th> <th>Cumul</th> <th>% Top</th>")
print("</tr>")

for tour in range(len(tab)) :
    print("<tr>")
    print("<td>%d</td>" % (tour+1))
    for nick in liste_nick :
        dic = tab[tour]
        if nick in dic :
            cum[nick] += dic[nick][2]
            val = (dic[nick][0], dic[nick][1], "%d"%dic[nick][2], "%d"%cum[nick], "%4.2f"%(cum[nick]/cum[nom_top]*100))
        else :
            val= ("&nbsp;",)*5
        print("""<td class="extr">%s</td> <td class="l">%s</td> <td >%s</td> <td >%s</td> <td >%s<s/td>""" % val)
    print("</tr>") 
print("</table>")
print("</html>")
