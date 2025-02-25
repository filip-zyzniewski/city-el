all: schematic.svg

schematic-scan.png: schematic-scan-1.png schematic-scan-2.png
	magick \
	-size 9320x6285 xc:black \
	\( schematic-scan-1.png -rotate -0.3 -geometry +0-20 \) -composite \
	\( schematic-scan-2.png -rotate 180 -geometry +4464-4 \) -composite \
	$@

clean:
	rm -f schematic-scan.png

open: schematic-scan.png
	open $^

