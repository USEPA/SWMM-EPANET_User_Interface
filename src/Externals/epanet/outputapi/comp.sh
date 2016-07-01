gcc -shared -o ENOutputAPI-64.so outputapi.c -g -O3 -fPIC -std=c99 -Wno-unused-result
# gcc test.c   -g -O3 -fPIC -std=c99 -c
# gcc  -g -O3 -fPIC -std=c99 -o prova test.o -loutputapi -L . -lm -Wl,-rpath,.
