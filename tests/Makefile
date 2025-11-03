
FC = gfortran
FCOPTS:=-c -cpp -ffree-line-length-none -ffree-form -J build
MODDIR:=build

rwildcard=$(wildcard $1$2) $(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2))

SOURCES := $(call rwildcard,src/,*.f90)
OBJS := $(patsubst %.f90,%.o,$(SOURCES))

all: $(OBJS) 

src/pointers.o : FCOPTS+=-fcray-pointer


%.o : %.f90
	$(FC) $(FCOPTS) -o $(subst src,build,$@) $<

.PHONY: clean

clean:
	rm -rf $(MODDIR)
	mkdir $(MODDIR)
	rm -rf src/*.mod src/*.o src/*.txt