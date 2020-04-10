::
::  before_build.bat - Prepares for swmm toolkit and output module builds
::
::  Date Created: 12/21/2018
::
::  Author: Michael E. Tryby
::          US EPA - ORD/NRMRL
::
:: Requires:
::     CMake
::     Visual Studio 2015
::     SWIG
::
:: Note:
::     This script must be located at the root of the project folder
:      in order to work correctly.
::


:: Determine project path and strip trailing \ from path
set "PROJECT_PATH=%~dp0"
IF %PROJECT_PATH:~-1%==\ set "PROJECT_PATH=%PROJECT_PATH:~0,-1%"

set "TOOLKIT_PATH=swmm_python\toolkit\swmm\toolkit"
set "OUTPUT_PATH=swmm_python\output\swmm\output"


:: Clone the project
mkdir buildlib
cd buildlib
git clone --branch=feature-wrapper https://github.com/michaeltryby/Stormwater-Management-Model.git swmm
cd swmm


:: Build the project
mkdir buildprod
cd buildprod
cmake -G"Visual Studio 14 2015 Win64" -DBUILD_TESTS=OFF ..
cmake --build . --config Release


:: Copy files required for python package build
copy /Y .\bin\Release\swmm5.dll  %PROJECT_PATH%\%TOOLKIT_PATH%
copy /Y .\lib\Release\swmm5.lib  %PROJECT_PATH%\%TOOLKIT_PATH%
copy /Y ..\include\*.h  %PROJECT_PATH%\%TOOLKIT_PATH%

copy /Y .\bin\Release\swmm-output.dll  %PROJECT_PATH%\%OUTPUT_PATH%
copy /Y .\lib\Release\swmm-output.lib  %PROJECT_PATH%\%OUTPUT_PATH%
copy /Y ..\tools\swmm-output\include\*.h  %PROJECT_PATH%\%OUTPUT_PATH%


:: Generate swig wrappers
cd %PROJECT_PATH%\%TOOLKIT_PATH%
swig -python -py3 toolkit.i
cd %PROJECT_PATH%\%OUTPUT_PATH%
swig -python -py3 output.i


:: Return to project root
cd %PROJECT_PATH%
