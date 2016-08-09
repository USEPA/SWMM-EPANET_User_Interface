C:\MinGW\bin\gcc -m64 outputapi.c -c
C:\MinGW\bin\gcc -m64 -shared -o SMOutputapi-64.dll outputapi.o
rem gcc test.c -c
rem gcc -o test.exe test.o -L. -l outputapi -lm
