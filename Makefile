SUBDIRS := \
	electronics/DCDC-CityCom-80501HF \
	electronics/GfE-BMS

TARGETS := all clean

$(TARGETS): $(SUBDIRS)
.PHONY: $(TARGETS) $(SUBDIRS)

$(SUBDIRS):
	make -C $@ $(MAKECMDGOALS)
