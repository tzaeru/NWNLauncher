import platform
import os.path
import config
import winreg
import os

NO_PATH = "Neverwinter Nights directory could not be resolved. Please set it manually."

cached_nwn_ini = ""
cached_exe_dir_path = NO_PATH

# Use subpath for accessing hak, override, etc, directories. Set null to access the root NWN directory.
def get_nwn_path(subpath="") -> str:
    global cached_nwn_ini

    # Open nwn.ini to memory
    if cached_nwn_ini == "":
        print("INI path: " + _find_ini_file())
        with open(_find_ini_file(), 'r') as myfile:
            cached_nwn_ini=myfile.read()

    if (len(subpath) > 0):
        for line in cached_nwn_ini.splitlines():
            if line.startswith(subpath.upper()):
                return line[line.find('=')+1:]

    return os.environ['USERPROFILE'] + "\\Documents\\Neverwinter Nights"

def set_nwn_path(path : str) -> bool:
    global cached_exe_dir_path
    cached_exe_dir_path = path

    return True

def get_server_config_path() -> str:
    return os.path.join("./config", config.current_server)

def get_server_images_path() -> str:
    return os.path.join("./config", config.current_server, "images")

def get_executable_path() -> str:
    global cached_exe_dir_path

    if platform.system() == "Windows":
        if cached_exe_dir_path == NO_PATH:
            cached_exe_dir_path = _find_executable_dir()
        return cached_exe_dir_path + "nwmain.exe"
    else:
        return os.path.join(get_nwn_path(), "nwmain")

def get_executable_dir_path() -> str:
    global cached_exe_dir_path

    if platform.system() == "Windows":
        if cached_exe_dir_path == NO_PATH:
            cached_exe_dir_path = _find_executable_dir()
        return cached_exe_dir_path

def get_config_path() -> str:
    return "./config";

def get_local_version_data_path() -> str:
    if not os.path.exists(os.path.join("./config", "file_info")):
        os.makedirs(os.path.join("./config", "file_info"))
    return os.path.join("./config", "file_info", config.local_versions_file)

def get_local_checksums_path() -> str:
    if not os.path.exists(os.path.join("./config", "file_info")):
        os.makedirs(os.path.join("./config", "file_info"))
    return os.path.join("./config", "file_info", config.local_checksums_file)

def get_cdkey_path() -> str:
    return os.path.join(get_nwn_path(), "cdkey.ini")

def get_nwnplayer_path() -> str:
    return os.path.join(get_nwn_path(), "nwnplayer.ini") 

def get_windows_hosts_path() -> str:
    return os.path.join("C:/Windows/System32/drivers/etc", "hosts") 

def get_logs_path() -> str:
    if platform.system() == "Windows":
        return os.path.join(get_nwn_path(), "logs")
    else:
        return None

def _find_executable_dir() -> str:
    registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
    try:
        # "Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 704450"
        # key = OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Steam App 704450", access=winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
        key = winreg.OpenKey(registry, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Steam App 704450", access=winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        path = winreg.QueryValueEx(key, "InstallLocation")[0] + "\\bin\\win32\\"
        return path
    except Exception as e:
        print("Key not found for executable, " + str(e))
    
    return NO_PATH

def _find_ini_file() -> str:
    return os.environ['USERPROFILE'] + "\\Documents\\Neverwinter Nights\\nwn.ini"