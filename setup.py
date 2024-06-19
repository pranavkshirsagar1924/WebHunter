from cx_Freeze import setup, Executable

# List of additional files to include
include_files = ['logo.ico']

# List of packages to include
packages = ["bs4", "requests", "shlex", "datetime", "os"]

setup(
    name="WebHunter",
    version="1.0",
    description="Scrap your static sites in sconds and then analyze data quickly",
    options={
        'build_exe': {
            'packages': packages,
            'include_files': include_files,
            'includes': [],
            'excludes': [],
            'optimize': 2,
            'path': []
        }
    },
    executables=[Executable("appy.py", icon="icon.ico")],  # Specify the icon file here
)
