from distutils.core import setup, Extension
setup(name="dico", version="1.02",
        author='Philippe Chataignon',
        author_email='philippe@chataignon.net',
        maintainer='Philippe Chataignon',
        url='www.chataignon.com',
    ext_modules=[
        Extension("dico", ["dico.c","dic.c"]),
    ])
