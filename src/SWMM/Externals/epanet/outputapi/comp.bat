rem Build ENOutputAPI-64.dll for 64-bit Windows using 64-bit MinGW
set PATH=C:\MinGW\bin
gcc -m64 outputapi.c -c
gcc -m64 -shared -o ENOutputAPI-64.dll outputapi.c
