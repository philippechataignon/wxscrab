rmdir /S /Q dist
c:\python26\python.exe setup.py py2exe -d dist
rmdir /S /Q build
copy wxscrab.nsi dist
copy msvcp90.dll dist
copy ..\client\GPL.txt dist
xcopy /S /E /Y ..\client\images dist\images\
xcopy /S /E /Y ..\client\skins dist\skins\
xcopy /S /E /Y ..\client\sound dist\sound\
cd dist
"C:\Program Files\NSIS\makeNSISw.exe" wxscrab.nsi
cd ..
rmdir /S /Q dist
