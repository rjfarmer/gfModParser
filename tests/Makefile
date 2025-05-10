
FC:=gfortran
FCOPTS:=-c -cpp -fcray-pointer -J build
MODDIR:=build

SRC:=src

BUILD:=build

SOURCES:=$(shell find $(SRC) -name '*.f90')
OBJS = $(patsubst %.f90,%.o,$(SOURCES))

all: $(OBJS) 

%.o : %.f90
	$(FC) $(FCOPTS) -o $(subst $(SRC),$(BUILD),$@) $<

