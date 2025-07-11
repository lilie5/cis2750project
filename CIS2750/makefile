CC = clang
CFLAGS = -Wall -pedantic -std=c99
PYTHON = python3.11
PYTHON_INCLUDE_PATH = /usr/include/python3.11
PYTHON_LIB_PATH = /usr/lib/python3.11

SWIG = swig

all: a2

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o -lm

phylib_wrap.c: phylib.h phylib.i
	$(SWIG) -python phylib.i

phylib.py: phylib.h phylib.i
	$(SWIG) -python phylib.i

phylib_wrap.o: phylib_wrap.c phylib.h
	$(CC) $(CFLAGS) -c phylib_wrap.c -I$(PYTHON_INCLUDE_PATH) -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) phylib_wrap.o -shared -L. -L$(PYTHON_LIB_PATH) -l$(PYTHON) -lphylib -o _phylib.so

a2: libphylib.so _phylib.so phylib.py

clean:
	rm -f *.o *.so *.svg phylib.py phylib_wrap.c