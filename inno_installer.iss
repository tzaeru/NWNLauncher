; -- Example2.iss --
; Same as Example1.iss, but creates its icon in the Programs folder of the
; Start Menu instead of in a subfolder, and also creates a desktop icon.

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=NWN Launcher
AppVersion=1
DefaultDirName={pf}\NWN Launcher
; Since no icons will be created in "{group}", we don't need the wizard
; to ask for a Start Menu folder name:
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\NWN Launcher.exe
OutputBaseFilename="NWN Launcher Installer"

[Files]
Source: "build/*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{commonprograms}\NWN Launcher"; Filename: "{app}\NWN Launcher.exe"
Name: "{commondesktop}\NWN Launcher"; Filename: "{app}\NWN Launcher.exe"
