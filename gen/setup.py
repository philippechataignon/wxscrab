from distutils.core import setup, Extension
setup(name="dico", version="1.01",
    ext_modules=[
        Extension("dico", ["dico.c","dic.c"]),
    ])
