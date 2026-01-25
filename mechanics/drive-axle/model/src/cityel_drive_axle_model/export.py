"""Exports models to files."""

import sys

import cadquery as cq

import cityel_drive_axle_model
import cityel_drive_axle_model.spline_cutter
import cityel_drive_axle_model.workplane

_MODELS = {
    "axle": cityel_drive_axle_model.PermThrige().build,
    "spline_cutter": cityel_drive_axle_model.spline_cutter.Tool.build,
}


def export(model_name: str, *file_names: str) -> None:
    """Export the model of a given name to given files."""
    builder = _MODELS[model_name]
    wp = cityel_drive_axle_model.workplane.Workplane("YZ")
    built = builder(wp)
    assembly = cq.Assembly()
    assembly.add(built, name=model_name)
    for file_name in file_names:
        assembly.export(file_name)


if __name__ == "__main__":
    export(*sys.argv[1:])
