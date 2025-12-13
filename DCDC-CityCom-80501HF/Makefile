all: schematic.svg

schematic.svg: schematic.kicad_sch
	docker run \
		--rm \
		--interactive \
		ghcr.io/kicad/kicad:9.0.6 \
		sh -c ' \
			cd ~ && \
			cat > $< && \
			kicad-cli sch export svg $< 1>&2 && \
			cat $@ \
		' < $< > $@

clean:
	rm -f schematic.svg
