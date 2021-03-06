import sys, os
from cx_Freeze import setup, Executable
import subprocess

subprocess.call("set TCL_LIBRARY=C:\Program Files (x86)\Python35-32\tcl\tcl8.6", shell=True)
subprocess.call("set TK_LIBRARY=C:\Program Files (x86)\Python35-32\tcl\tk8.6", shell=True)

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"build_exe":"build",
"packages": ["os"],
"include_files":[("config/potm", "config/potm"),
("config/main_config.toml", "config/main_config.toml"),
("winmtr", "winmtr")]}

#("windows_manifest.xml", "NWN Launcher.xml.manifest")

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "guifoo",
        version = "0.1",
        description = "My GUI application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base, targetName="NWN Launcher.exe", icon="ICO/nwn_composite_RA8_icon.ico")])

subprocess.call('mt -manifest windows_manifest.xml -outputresource:"build/NWN Launcher.exe"', shell=True)

os.remove("build/tk/images")
os.remove("build/tk/demos")
os.remove("build/tcl/tzdata")