MODEL_FORMATS=glb step stl
MODEL_NAMES=axle spline_cutter

MODEL_EXPORT_FILES=$(foreach name,$(MODEL_NAMES),$(addprefix $(name).,$(MODEL_FORMATS)))

.PHONY: clean lint

%.glb %.step %.stl &:
	uv run -m cityel_drive_axle_model.export $* $*.glb $*.step $*.stl

all: lint $(MODEL_EXPORT_FILES)

clean:
	rm -f $(MODEL_EXPORT_FILES)

lint:
	uv run ruff check src
	uv run ruff format --check --diff src

