from distutils.core import setup, Extension

module1 = Extension('output',
                    sources = ['swmm_output.c','output_wrap.c','errormanager.c'])

setup (name = 'output',
       version = '1.0',
       description = 'SWMM output package',
       ext_modules = [module1])
