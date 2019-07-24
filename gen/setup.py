from distutils.core import setup, Extension
setup(name="dic", version="2.0.0",
    author='Philippe Chataignon',
    author_email='philippe@chataignon.net',
    maintainer='Philippe Chataignon',
    url='www.chataignon.com',
    ext_modules=[Extension(name="_dic", sources=["dic_wrap.c","dic.c"])],
    py_modules=["dic"]
)
