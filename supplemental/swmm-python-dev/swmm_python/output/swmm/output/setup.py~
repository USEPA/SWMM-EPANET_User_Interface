# -*- coding: utf-8 -*-

#
# setup.py - Setup script for swmm_output python extension
#
# Created:    7/2/2018
# Author:     Michael E. Tryby
#             US EPA - ORD/NRMRL
#
# Requires:
#   Platform C language compiler
# Modified 8 April 2020 by Erik Beck, USEPA Region One


from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


setup(
    name = 'swmm.output',
    version = "0.4.0.dev1",

    ext_modules = [
        Extension("swmm.output._output",
            sources = ['output_wrap.c'],
            include_dirs = ['swmm/output/'],
            libraries = ['swmm-output'],
            library_dirs = ['swmm/output/'],
            language='C'
        )
    ],
    # tox can't find swmm module at test time unless namespace is declared
    namespace_packages = ['swmm'],

    packages = ['swmm.output'],
    py_modules = ['output'],
    package_data = {'swmm.output':['./*swmm-output.dll', './*swmm-output.so']},

    zip_safe=False,

    install_requires = [
        'aenum'
    ]
)
