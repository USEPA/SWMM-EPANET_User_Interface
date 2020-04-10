

import os
import pathlib

from six import iteritems

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


import sys
import subprocess


PACKAGE_NAME = 'swmm'
SOURCES = {
  'swmm.toolkit': 'swmm_python/toolkit',
  'swmm.output': 'swmm_python/output'
}


def install_microlibs(sources, develop=False):
    """ Use pip to install all microlibraries.  """
    print("installing all microlibs in {} mode".format("development" if develop else "normal"))
    wd = pathlib.Path.cwd()
    for k, v in iteritems(sources):
        try:
            microlib_dir = os.fspath(wd.joinpath(v))
            if develop:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-e', '.'], cwd=microlib_dir)
            else:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '.'], cwd=microlib_dir)
        except Exception as e:
            print("Oops, something went wrong installing", k, microlib_dir)
            print(e)
        finally:
            os.chdir(wd)


class DevelopCmd(develop):
    """ Add custom steps for the develop command """
    def run(self):
        install_microlibs(SOURCES, develop=True)
        develop.run(self)


class InstallCmd(install):
    """ Add custom steps for the install command """
    def run(self):
        install_microlibs(SOURCES, develop=False)
        install.run(self)


setup(
    name=PACKAGE_NAME,
    version="0.3.0.dev1",

    cmdclass={
        'install': InstallCmd,
        'develop': DevelopCmd
    },

    author="Michael Tryby",
    author_email="Michael Tryby@epa.gov",
    description="swmm_python - SWIG generated python wrappers for swmm libraries",
    license="CC0",
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],

    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest==4.2.0',
        'numpy'
    ]
)
