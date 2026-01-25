SUBDIRS := \
	electronics/DCDC-CityCom-80501HF \
	electronics/GfE-BMS \
	mechanics/drive-axle/model

TARGETS := all clean lint

$(TARGETS): $(SUBDIRS)
.PHONY: $(TARGETS) $(SUBDIRS)

$(SUBDIRS):
	make -C $@ $(MAKECMDGOALS)
