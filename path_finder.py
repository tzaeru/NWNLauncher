import platform

paths_for_windows = [
	"C:/NWN",
	"C:/Program Files/NWN",
	"C:/Program Files/NeverwinterNights",
	"C:/Program Files(x86)/NWN",
	"C:/Program Files(x86)/NeverwinterNights",
	"C:/Games/NWN",
	"C:/Games/NeverwinterNights",
]

def get_path() -> str:
	if platform.system() == "Windows":
		return _get_path_win32
	else:
		return "Automatic path resolvement for non-Windows systems isn't supported yet."

def _get_path_win32() -> str:
