# NWNLauncher
A generic multiplatform launcher and dependency downloader for Neverwinter Nights. The launcher is meant to be customized per-server and distributed as a standalone or an installer by the server.

Work in progress! Files can currently be lost. Made to be multiplatform, but not tested on Linux nor OS X!

## Features

* Automatically finds NWN's path on Windows. WIP: Linux and OS X support.
* Downloads dependencies (haks, erfs, tlks, overrides, portraits..).
* Able to update dependencies per-file according to a checksum or a version number.
* Configurable to various styles of distribution. You can use a custom file server or even NWVault for dependencies.
* Recognizes if the user is using the default GoG.com CD key and warns about it.
* Can write to Windows hosts file to speed up launch.
* Supports both PC and DM connections.
* Checkboxes for whether to download overrides, music, portraits.
* Multiple server configurations per one launcher. Simply choose your server from a drop-down!
* Picks the server IP from a remote configuration file; Can change server IP without reinstalling NWN Launcher.

## Usage

Download the pre-created launcher template [some url](www.google.fi) and extract.

### Quick guide
* Setup a file server. [NWNLauncher Backend](https://github.com/tzaeru/NWNLauncher-Backend) is recommended but not necessary.
* Copy your haks, erfs, tlks, overrides, music, portraits to your file server, preferrably behind `hak`, `erf`, etc directories.
* Customize your `files.toml` in the root of your file server.
* Change `local_versions_file` in your launcher bundle's `config.toml`
* Change `remote_data_file` in your launcher bundle's `config.toml` to your `files.toml` URL.
* Change `nwn_server_address` in your launcher bundle's `config.toml` to your NWN server's address.
* Replace the images in `images/` of the launcher template with your own customized images.

**The recommended way** of distributing the dependencies of your server is by providing them online. For this, NWN Launcher needs a `files.toml` file, which describes the set of files. Any file server can be used for the purpose of serving the files online, though [NWNLauncher Backend](https://github.com/tzaeru/NWNLauncher-Backend) is a slim file server project tailored specifically for NWNLauncher.

The defaut `files.toml` should look something like this:
  ```toml
    server_ip = "104.155.20.124:5121"

    [[files]]
    name = "cep2_add_doors.hak"
    version = 1
    url = "~hak/cep2_add_doors.hak"
    target_dir = "hak"
    target_file = "cep2_add_doors.hak"
    checksum = "555889644a83c4ceaabf7f8f27c762be"

    [[files]]
    name = "cep2_add_loads.hak"
    version = 1
    url = "~hak/cep2_add_loads.hak"
    target_dir = "hak"
    target_file = "cep2_add_loads.hak"
    checksum = "03f0a763fa1c4f15366ee3dda86bfc58"
  ```
  
`~` before `url` indicates an URL relative to the location of `files.toml`. So, if your `files.toml` was provided at `www.some_url.com/files/files.toml`, then the resolved path would be `www.some_url.com/files/hak/cep2_add_doors.hak` for the file `cep2_add_doors.hak`. Full URLs can be also used; In this case, simply omit the wiggly. For full documentation of the variables in `files.toml`, check [some url](www.google.fi).

The `server_ip` is the IP of the Neverwinter Nights server to connect to.

Once your files are available, open `config.toml` in the root of the template directory you extracted earlier and change the `remote_data_file` config variable to point to the full URL of your `files.toml` file. Now is a good time to also change `nwn_server_address` in `config.toml` to match the address of your NWN server. This address will be used if `files.toml` is unavailable.


## Development
You can also fork the sources of the project and create your own version of it.

### Dependencies

Currently, the only dependency in addittion to Python 3.4 is pytoml (pip install pytoml)


## License

WTFPL
