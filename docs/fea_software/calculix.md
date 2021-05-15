# Calculix

```{contents} Table of Contents
:local: 
:depth: 1
```
## Setup and compilation from source
To use Calculix in multithreading mode it is needed to compile from source. In order to do so it is necessary to compile ARPACK and SPOOLES library and install the required tools. The code which is presented here is already changed and ready for compilation. Please read the original documentation first from [here](http://www.dhondt.de/ccx_2.17.README.INSTALL).

### Tools
1. Install the required tools for Calculix:
    -   gfortran
    -   make
    -   f2c
    -   liblapack3
    -   liblapack-dev
    -   libexodusii-dev
    -   libgl1-mesa-dev
    -   libglu1-mesa-dev
    -   libxi-dev
    -   libxmu-dev
    -   gcc

using your package manager. For Ubuntu and Debian-oriented system the command should be like:

```
sudo apt-get install gfortran make f2c liblapack3 liblapack-dev libexodusii-dev libgl1-mesa-dev libglu1-mesa-dev libxi-dev libxmu-dev
```
### SPOOLES

SPOOLES library should be obtained from this [site](http://www.netlib.org/linalg/spooles/spooles.2.2.tgz) using wget command.

```
wget http://www.netlib.org/linalg/spooles/spooles.2.2.tgz
```

After downloading the file, it is mandatory to create folder SPOOLES.2.2. Move the archive there and unpack it. It can be done with the following commands:

```
mkdir SPOOLES.2.2
mv spooles.2.2.tgz SPOOLES.2.2
cd SPOOLES.2.2
tar xvf spooles.2.2.tgz
```
Change directory to SPOOLES.2.2 with cd:

```
cd SPOOLES.2.2
```

Then  uncomment 14 line and comment line 15 in Make.inc file with your text editor. It can be done by:

```
gedit Make.inc
```
The file after changes should look like:

```
CC = gcc
#  CC = /usr/lang-4.0/bin/cc
```
Now the files are ready for compilation. Use:

```
make lib  
```
Then it is needed to compile the MT library. It is done with following commands:

```
cd MT/src/
make   
```
### ARPACK

Next step is to compile ARPACK library. It is needed to download 2 separate archives. Obtain it from [here](https://www.caam.rice.edu/software/ARPACK/SRC/arpack96.tar.gz) and [here](https://www.caam.rice.edu/software/ARPACK/SRC/patch.tar.gz).


```
wget https://www.caam.rice.edu/software/ARPACK/SRC/arpack96.tar.gz
wget https://www.caam.rice.edu/software/ARPACK/SRC/patch.tar.gz
```

Then unpack files with tar commands

```
tar xvf arpack96.tar.gz
tar xvf patch.tar.gz
```

- In `ARPACK/ARmake.inc` change:
    -   `home = $(HOME)/ARPACK` to your ARPACK directory
    -   `PLAT = SUN4` to `PLAT = linux`
    -   `FC = f77` to `FC = gfortran`
    -   `FFLAGS = -O -cg89` to `FFLAGS = -O2`
    -   `MAKE = /bin/make` to `MAKE = make`
    -   `SHELL = /bin/sh` to `SHELL = shell`
- In `ARPACK/UTIL/second.f` change: `EXTERNAL ETIME` to `*EXTERNAL ETIME`

Then mowe to ARPACK directory and run:

```
make lib   
```
### Calculix compilation

Obtain Calculix [source code](http://www.dhondt.de/ccx_2.17.src.tar.bz2) using wget to your Calculix directory.

```
wget http://www.dhondt.de/ccx_2.17.src.tar.bz2
```
To unpack archieve use:
```
bunzip2 ccx_2.17.src.tar.bz2
tar xvf ccx_2.17.src.tar
```
In order to compile Calculix in multithreading mode it is needed to change the Makefile from singlethread to multithread one. It can be simply done by:

```
cd CalculiX/ccx_2.17/src
mv Makefile Makefile_ST
mv Makefile_MT Makefile
```
- In `Makefile` change:
    -   `CC=cc` to `CC=gcc`
    - in 15 line   `../../../ARPACK/libarpack_INTEL.a \` to `../../../ARPACK/libarpack_linux.a \`

Then it is possible to compile Calculix with:

```
make
```
Happy meshing!

## Interesting projects with CalculiX

[CAE](https://github.com/calculix/cae) is a software package mainly consisting of CalculiX GraphiX, CrunchiX and keyword editor.

[unv2ccx](https://github.com/calculix/unv2ccx) is a mesh converter that allows to convert Salome UNV file into CalculiX INP file.

[ccx2paraview](https://github.com/calculix/ccx2paraview) is a Calculix results converter which creates a Paraview compatible file.

[pycalculix](https://github.com/spacether/pycalculix) is a Python 3 library to automate and build finite element analysis (FEA) models in Calculix.

