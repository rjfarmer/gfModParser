
FC:=gfortran
FCOPTS:=-c -cpp -fcray-pointer -J build
MODDIR:=build

rwildcard=$(wildcard $1$2) $(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2))

SOURCES := $(call rwildcard,src/,*.f90)
OBJS := $(patsubst %.f90,%.o,$(SOURCES))

all: $(OBJS) 

%.o : %.f90
	$(FC) $(FCOPTS) -o $(subst src,build,$@) $<

.PHONY: clean

clean:
	rm -rf $(MODDIR)
	mkdir $(MODDIR)
