all: board-schematic.svg connection-schematic-scan.png

board-schematic.svg: board-schematic.kicad_sch
	kicad-cli sch export svg $<

clean:
	rm -f board-schematic.svg
