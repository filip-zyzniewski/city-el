all: schematic.svg

schematic.svg: schematic.kicad_sch
	kicad-cli sch export svg $<

clean:
	rm -f schematic.svg
