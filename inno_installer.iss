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
ChangesAssociations=yes

[Files]
Source: "build/*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "ICO/*"; DestDir: "{app}";

[Icons]
Name: "{commonprograms}\NWN Launcher"; Filename: "{app}\NWN Launcher.exe"
Name: "{commondesktop}\NWN Launcher"; Filename: "{app}\NWN Launcher.exe"

[Registry]
Root: HKCR; Subkey: ".nwnl"; ValueType: string; ValueName: ""; ValueData: "NWNLauncherServerFile"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "NWNLauncherServerFile"; ValueType: string; ValueName: ""; ValueData: "NWN Launcher Server File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "NWNLauncherServerFile\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\NWN Launcher.exe,0"
Root: HKCR; Subkey: "NWNLauncherServerFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\NWN Launcher.exe"" ""%1"""
