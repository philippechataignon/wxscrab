import os

class logger :
    def __init__(self, fichier) :
        dir = "log"
        self.file = open(os.path.join(dir, fichier),"w")
        self.file.write("""<?xml version="1.0"?>\n""")
        self.file.write("""<partie nom="%s">\n""" % fichier)

    def add_prop(self, nick, coo, mot, score, temps) :
        self.file.write("""
    <prop>    
        <nick>%s</nick>
        <coord>%s</coord>
        <mot>%s</mot>
        <score>%d</score>
        <temps>%d</temps>
    </prop>
    """ % (nick, coo, mot, score, temps))

    def debut_tour(self, tour) :
        self.file.write("""\n<tour num="%d">\n""" % tour)

    def fin_tour(self, cc, mm, pts) :
        self.file.write("""
    <top>
        <coord>%s</coord>
        <mot>%s</mot>
        <score>%d</score>
    </top>
</tour> 
        """ % (cc, mm, pts))

    def fin_partie(self) :
        self.file.write("</partie>\n")
        self.file.close()
