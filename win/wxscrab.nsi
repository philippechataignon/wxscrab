!define /date MyTIMESTAMP "%Y%m%d_%H%M"
!include MUI2.nsh

; The name of the installer
XPStyle on
Name "wxScrab"

; The file to write
OutFile "../setup_wxscrab_${MyTIMESTAMP}.exe"

; The default installation directory
InstallDir $PROGRAMFILES\wxScrab

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\wxScrab" "Install_Dir"

!define MUI_ABORTWARNING
; Pages

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "GPL.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;Languages
 
  !insertmacro MUI_LANGUAGE "French"


; Sections

Section "wxScrab" main

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File /r *.*
     
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\wxScrab "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\wxScrab" "DisplayName" "wxScrab (suppression)"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\wxScrab" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\wxScrab" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\wxScrab" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Raccourcis menu Démarrer" menu
  CreateDirectory "$SMPROGRAMS\wxScrab"
  CreateShortCut "$SMPROGRAMS\wxScrab\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\wxScrab\wxScrab.lnk" "$INSTDIR\wxscrab.exe" "" "$INSTDIR\wxScrab.exe" 0
SectionEnd


;Descriptions

  ;Language strings
  LangString DESC_main ${LANG_FRENCH} "Installer le jeu wxScrab"
  LangString DESC_menu ${LANG_FRENCH} "Mettre des raccourcis dans le menu Démarrer"

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${main} $(DESC_main)
    !insertmacro MUI_DESCRIPTION_TEXT ${menu} $(DESC_menu)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\wxScrab"
  DeleteRegKey HKLM SOFTWARE\wxScrab
  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\wxScrab\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\wxScrab"
  RMDir /r "$INSTDIR"

SectionEnd
