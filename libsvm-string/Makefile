CXX ?= g++
CFLAGS = -Wall -Wconversion -O3 -fPIC -D _STRING
SHVER = 2

LIBS = svm.o subsequence.o

all: svm-train svm-predict svm-scale lib kernel-test

lib: svm.o
	$(CXX) -shared -dynamiclib $(LIBS) -o libsvm.so.$(SHVER)

svm-predict: svm-predict.c svm.o
	$(CXX) $(CFLAGS) svm-predict.c $(LIBS) -o svm-predict -lm
svm-train: svm-train.c svm.o
	$(CXX) $(CFLAGS) svm-train.c $(LIBS) -o svm-train -lm
svm-scale: svm-scale.c
	$(CXX) $(CFLAGS) svm-scale.c -o svm-scale
svm.o: svm.cpp svm.h subsequence.o
	$(CXX) $(CFLAGS) -c svm.cpp
subsequence.o: subsequence.cpp subsequence.h
	$(CXX) $(CFLAGS) -c subsequence.cpp
kernel-test: kernel-test.cpp subsequence.o
	>~$(CXX) $(CFLAGS) kernel-test.cpp subsequence.o -o kernel-test

clean:
	rm -f *~ $(LIBS) svm-train svm-predict svm-scale kernel-test libsvm.so.$(SHVER)
