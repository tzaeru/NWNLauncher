import path_finder
import os, sys
import platform

# Check if hosts entry is already added.
def _check_authentication_skip():
    if platform.system() == "Windows":
        hosts = None
        try:
            with open(path_finder.get_windows_hosts_path()) as hosts_file:
                hosts = hosts_file.read()

                if hosts.find("nwmaster") >= 0:
                    return True
                if hosts.find("NWN") >= 0:
                    return True

            return False
        except err:
            print("Couldn't open hosts file..")

    return False

# Add hosts entry to skip NWN authentication.
def _add_authentication_skip():
    if platform.system() == "Windows":
        hosts = None

        try:
            with open(path_finder.get_windows_hosts_path()) as hosts_file:
                hosts = hosts_file.read()

                #Early bails to avoid writing twice to it
                if hosts.find("nwmaster") >= 0:
                    return False
                if hosts.find("NWN") >= 0:
                    return False

                hosts += "\n# NWN entry to skip authentication attempts to NWN master server\n"
                hosts += "0.0.0.0 nwmaster.bioware.com"
                hosts += "\n\n"
                
            if hosts is not None:
                f = open(path_finder.get_windows_hosts_path(),'w')
                f.write(hosts)
                f.flush()
                f.close()
                return True
        except:
            print("Couldn't open hosts file..")

    return False
