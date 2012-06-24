#TODO:
#common options (-Wall)
#find compiler
#CFLAGS and so on
#detect python version

all: liblyricseek.so	lyricseek_test

liblyricseek.so: lyricseek.os
	gcc -o liblyricseek.so -shared lyricseek.os -lpython2.7
lyricseek_test: test.o
	gcc -o lyricseek_test test.o -L. -llyricseek -lpython2.7


lyricseek.os: lyricseek.c lyricseek.h
	gcc -o lyricseek.os -c -DDEBUGGING -I`python2.7-config --includes --libs --cflags` lyricseek.c

test.o: test.c
	gcc -o test.o -c -DDEBUGGING -I`python2.7-config --includes --libs --cflags` test.c

clean:
	rm test.o lyricseek.os lyricseek_test liblyricseek -f
