Install SWIG SWMM Output API from wheel

    Click to download SWIG SWMM Output API wheel file: swmm.output-0.4.0.dev2-cp37-cp37m-win_amd64.whl and save it to a directory of your choosing.

    Inside PyCharm, open python console (Tools-> Python Console... menu option), then type in the following code to install the downloaded SWMM output api whl:

import pip
def install_whl(path):
    pip.main(['install', path])

wpath = "C:/path/to/whl/file/swmm.output-0.4.0.dev2-cp37-cp37m-win_amd64.whl"
install_whl(wpath)


