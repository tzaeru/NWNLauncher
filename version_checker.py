import config
from urllib.request import urlopen

available_version = None
current_version = 0
def get_available_version():
    response = urlopen(config.launcher_version_address)
    data = response.read()
    version = int(data.decode("utf-8"))
    print("Version number: " + str(version))

    global available_version
    available_version = version

def is_update_available() -> bool:
    if available_version == None:
        return False

    if available_version > current_version:
        return True
    else:
        return False