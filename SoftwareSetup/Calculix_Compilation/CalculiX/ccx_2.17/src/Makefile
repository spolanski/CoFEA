
CFLAGS = -Wall -O2 -fopenmp -I ../../../SPOOLES.2.2 -DARCH="Linux" -DSPOOLES -DARPACK -DMATRIXSTORAGE -DUSE_MT=1 
FFLAGS = -Wall -O2 -fopenmp 

CC=gcc
FC=gfortran

.c.o :
	$(CC) $(CFLAGS) -c $<
.f.o :
	$(FC) $(FFLAGS) -c $<

include Makefile.inc

SCCXMAIN = ccx_2.17.c

OCCXF = $(SCCXF:.f=.o)
OCCXC = $(SCCXC:.c=.o)
OCCXMAIN = $(SCCXMAIN:.c=.o)

DIR=../../../SPOOLES.2.2

LIBS = \
       $(DIR)/MT/src/spoolesMT.a \
       $(DIR)/spooles.a \
       ../../../ARPACK/libarpack_linux.a \
       -lpthread -lm

ccx_2.17_MT: $(OCCXMAIN) ccx_2.17_MT.a  $(LIBS)
	./date.pl; $(CC) $(CFLAGS) -c ccx_2.17.c; $(FC) -fopenmp -Wall -O2 -o $@ $(OCCXMAIN) ccx_2.17_MT.a $(LIBS)

ccx_2.17_MT.a: $(OCCXF) $(OCCXC)
	ar vr $@ $?
                                                                               
