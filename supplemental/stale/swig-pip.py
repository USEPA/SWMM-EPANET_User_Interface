# Erik Beck
# April 8, 2020
# installing output from swig

import pip
def install_whl(path):
    pip.main(['install', path])

wpath = "./swmm.output-0.4.0.dev2-cp37-cp37m-win_amd64.whl"
install_whl(wpath)
