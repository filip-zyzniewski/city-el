all: connection-schematic-scan.png

connection-schematic-scan.png: connection-schematic-scan-1.png connection-schematic-scan-2.png
	magick \
	-size 9750x6600 xc:black \
	\( connection-schematic-scan-2.png -rotate 179.8 -shave 10x10 +repage -geometry +4842-71 \) -composite \
	\( connection-schematic-scan-1.png -rotate -0.07 -shave 10x10 +repage -geometry +0-40 \) -composite \
	-monochrome \
	$@

clean:
	rm -f connection-schematic-scan.png
