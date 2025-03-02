## Copyright (c) 2019 alberto Otero de la Roza <aoterodelaroza@gmail.com>
## This file is frere software; distributed under GNU/GPL version 3.

## Originally URL https://aoterodelaroza.github.io/devnotes/modern-fortran-makefiles/

## no implicit rules
.SUFFIXES: 
FORTEXT:=f90 F90

## definitions
FC=gfortran
COMPILE.f08 = $(FC) $(FCFLAGS) $(TARGET_ARCH) -c
MAKEMOD.f08 = $(FC) $(FCFLAGS) $(TARGET_ARCH) -fsyntax-only -c

## mod and smod directory
MODDIR := build
ifneq ($(MODDIR),)
  $(shell test -d $(MODDIR) || mkdir -p $(MODDIR))
  FCFLAGS+= -J $(MODDIR)
endif

# $(call source-to-extension,source-file-list,new-extension)
define source-to-extension
  $(strip \
    $(foreach ext,$(FORTEXT),\
      $(subst .$(ext),.$2,$(filter %.$(ext),$1))))
endef
# $(call modsource-pattern-rule,extension)
define modsource-pattern-rule
%.anc: %.$1
	$$(MAKEMOD.f08) $$<
	@touch $$@
endef

## sources for the program
SOURCES:=$(wildcard src/*.f90)
OBJECTS:=$(call source-to-extension,$(SOURCES),o)
ANCHORS:=$(call source-to-extension,$(SOURCES),anc)

## main and clean targets
main: $(OBJECTS)
	$(FC) -c -cpp $@ $+

.PHONY: clean
clean:
	-rm -rf *.mod *.smod $(OBJECTS) $(ANCHORS) 
	-test -d $(MODDIR) && rm -r $(MODDIR)

## compilation rules
$(foreach ext,$(FORTEXT),$(eval $(call modsource-pattern-rule,$(ext))))
%.o: %.anc
	$(COMPILE.f08) $(OUTPUT_OPTION) $(wildcard $(addprefix $*.,$(FORTEXT)))
	@touch $@
