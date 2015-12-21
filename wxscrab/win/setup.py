from distutils.core import setup

import sys
sys.path.append('../client')
sys.path.append('../common')

import py2exe

setup(
    version = "1.0",
    description = "Client scrabble wxScrab",
    name = "wxScrab",

    # targets to build
    windows = [{"script" : "../client/go.py", "icon_resources":[(0,"../client/images/wxscrab.ico")]}],
    )
