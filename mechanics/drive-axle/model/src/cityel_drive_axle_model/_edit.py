"""Script starting CQ-editor with the model loaded."""

import sys

import cadquery as cq
import cq_editor.cqe_run

box = cq.Workplane("front").box(4, 2, 1)

if "show_object" in globals():
    # ruff: noqa: F821
    show_object(
        box,
        name="box",
        options={"color": (255, 0, 0)},
    )


def run() -> None:
    sys.argv.append(__file__)
    sys.exit(cq_editor.cqe_run.main())
