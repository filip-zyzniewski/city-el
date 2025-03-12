ALL = schematic.svg pcb-components-embedded.svg

all: $(ALL)

schematic.svg: schematic.kicad_sch
	kicad-cli sch export svg $<

%-embedded.svg: %.svg
	../tools/svg_embed_images.py $< > $@

clean:
	rm -f $(ALL)
