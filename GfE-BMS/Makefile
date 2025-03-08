all: schematic-scan.png

schematic-scan.png: schematic-scan-1.png schematic-scan-2.png
	magick \
	-size 9750x6600 xc:black \
	\( schematic-scan-2.png -rotate 179.8 -shave 10x10 +repage -geometry +4842-71 \) -composite \
	\( schematic-scan-1.png -rotate -0.07 -shave 10x10 +repage -geometry +0-40 \) -composite \
	-monochrome \
	$@

clean:
	rm -f schematic-scan.png
