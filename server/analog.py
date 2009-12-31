#!/usr/bin/env python2.5
from __future__ import division
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
print """
<table style="border: 1px solid" cellpadding="2">
  <tr>
  <th style="border: 1px solid">Tour</th>
"""
for nick in liste_nick :
    cum[nick] = 0 
    print """<th colspan="5"  style="border: 1px solid">%s</th>""" % nick
print """
  </tr>
  <tr>
  <td>&nbsp;</td>
"""
for nick in liste_nick :
    print """<th  style="border-left: 1px solid; border-bottom: 1px solid" >Coord</th>
                 <th  style="border-left: 1px dashed; border-bottom: 1px solid">Mot</th>
                 <th  style="border-left: 1px dashed; border-bottom: 1px solid; text-align:right">Score</th>
                 <th  style="border-left: 1px dashed; border-bottom: 1px solid; text-align:right">Cumul</th>
                 <th  style="border-left: 1px dashed; border-bottom: 1px solid; text-align:right">% Top</th>"""
print "</tr>"

for tour in xrange(len(tab)) :
    print "<tr>"
    print "<td>%d</td>" % (tour+1)
    for nick in liste_nick :
        dic = tab[tour]
	if nick in dic :
		cum[nick] += dic[nick][2]
		print """<td  style="border-left: 1px solid; text-align:center" >%s</td>
			 <td  style="border-left: 1px dashed">%s</td>
			 <td  style="border-left: 1px dashed; text-align:right">%d</td>
			 <td  style="border-left: 1px dashed; text-align:right">%d</td>
			 <td  style="border-left: 1px dashed; text-align:right">%4.2f</td>""" \
		    % (dic[nick][0], dic[nick][1], dic[nick][2], cum[nick], cum[nick]/cum[nom_top]*100)
    print "</tr>"


print """
</table>
"""
