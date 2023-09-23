from distutils.core import setup
import py2exe

setup(
    windows = [{"script":"srpg.py","icon_resources": [(0, "icon.ico")]}],
    data_files = [ (".", ["README.txt", "bsd_license.txt"]) ],
    options = {'py2exe':{'excludes':["wx",'email',"Tkconstants","Tkinter","tcl","numpy"],
        'bundle_files':1} # Unbreaks the music
        }
    )
