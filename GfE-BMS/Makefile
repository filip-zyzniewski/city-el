all: schematic.svg

schematic-scan.png: schematic-scan-1.png schematic-scan-2.png
	magick \
	-size 9750x6600 xc:black \
	\( schematic-scan-2.png -rotate 179.8 -shave 10x10 +repage -geometry +4842-71 \) -composite \
	\( schematic-scan-1.png -rotate -0.07 -shave 10x10 +repage -geometry +0-40 \) -composite \
	$@

# potrace works better with a scaled down image
schematic-scan.pgm: schematic-scan.png
	magick $< -scale 30% $@

schematic-scan.svg: schematic-scan.pgm
	potrace -a 0 $< -b svg -o $@

clean:
	rm -f \
	schematic-scan.png \
	schematic-scan.pgm \
	schematic-scan.svg

open: schematic-scan.svg
	open $^

