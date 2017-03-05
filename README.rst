wxScrab
=======

Résumé
------

wxScrab regroupe 3 programmes :

* un générateur de parties construit à partir du programme Eliot 
  (http://www.nongnu.org/eliot/), qui, à partir d'un partir d'un dictionnaire
  au format dawg génère un fichier XML. L'apport par rapport à Eliot est l'ajout
  d'un algorithme de choix parmi les différents tops possibles (isotops). Le
  générateur comprend également la construction d'un module Python en C pour
  accéder au dictionnaire et permettre de vérifier l'existence d'un mot (module
  dico). Les programmes sont dans le répertoire gen et le script install
  automatise la construction (et comprend un sudo pour installer le module
  Python)

* un serveur qui, à partir d'un fichier "partie" généré à l'étape précédente, va
  gérer la partie, en particulier l'arbitrage des différents clients. Le serveur
  est écrit en Python et s'appuie sur twisted. Les programmes sont dans le
  répertoire server

* un client graphique qui peut se connecter au serveur. Le programme est écrit
  en Python et fait appel à la libraire wxPython. Pour jouer sur un serveur
  existant, comme le serveur public wxscrab.ath.cx, port 12345, c'est le seul
  programme nécessaire.

Dépendances (pour Debian/Ubuntu)
--------------------------------

* générateur + module dico en Python : build-essential python-dev

* server : python-twisted (et module dico du générateur)

* client : python-wxgtk2.8 python-yaml

Lancement du client
-------------------

Dans un terminal, entrer les commandes suivantes ::

    cd wxscrab/client
    ./go.py


Lancement du serveur
--------------------

Dans un terminal, entrer les commandes suivantes ::

    cd wxscrab/server
    ./go.py

English
=======

summary
-------

wxScrab includes three programs:

* A generator built from parts of the program Eliot
   (http://www.nongnu.org/eliot/), which, from a dictionary in
   dawg format generates an XML file. 

   The contribution from Eliot is the addition of
   an algorithm of choice among different possible tops. The
   generator also includes a Python module in C for
   access the dictionary and verify the existence of a word (module
   dico). The programs are in the gen directory and the install script
   automates the construction (and includes a sudo to install the module
   Python)

* A server that is, from a file "part" generated in the previous step, will
   manage the game. The server is written in Python and uses Twisted. 

* A GUI client that can connect to the server. The program is written
   in Python and uses the wxPython library. To play on a existing server,
   as the public server wxscrab.ath.cx, port 12345, this is the only
   program required.

Dependencies (for Debian / Ubuntu)
----------------------------------

* Module dico generator in Python: build-essential python-dev

* Server: python-twisted (and module generator dico)

* Client: python python-yaml-wxgtk2.8

Launching the client
--------------------

In a terminal, enter the following commands ::

     wxscrab cd / customer
     . / go.py


Server start
------------

In a terminal, enter the following commands ::

     wxscrab cd / server
     . / go.py
