"""Script starting CQ-editor with the model loaded."""

import sys

import cq_editor.cqe_run

import cityel_drive_axle_model
import cityel_drive_axle_model.spline_cutter
import cityel_drive_axle_model.workplane

if "show_object" in globals():
    wp = cityel_drive_axle_model.workplane.Workplane("YZ")
    axle = cityel_drive_axle_model.PermThrige().build(wp)
    wp = wp.transformed(offset=(50, 0, 0))
    spline_cutter_tool = cityel_drive_axle_model.spline_cutter.Tool.build(wp)
    # ruff: noqa: F821
    show_object(
        spline_cutter_tool,
        name="spline cutter tool",
    )
    show_object(
        axle,
        name="drive axle",
    )


def run() -> None:
    sys.argv.append(__file__)
    sys.exit(cq_editor.cqe_run.main())
