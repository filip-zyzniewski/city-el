"""Deutsches Institut für Normung standards."""

import math

import cadquery as cq

import cityel_drive_axle_model.workplane


def d332a5(
    wp: cityel_drive_axle_model.workplane.Workplane,
) -> cityel_drive_axle_model.workplane.Workplane:
    """Return a DIN 332-A-5 centering hole cutout.

    Reference: https://www.scribd.com/doc/32703860/DIN-332-A-Centering-Holes-60g
    """
    # A1,6 x 3,35
    d1 = 1.6
    r1 = d1 / 2
    angle1 = math.radians(120)
    d2 = 3.35
    r2 = d2 / 2
    angle2 = math.radians(60)
    t = 2.9
    cone1_depth = r1 / math.tan(angle1 / 2)
    cone2_depth = (r2 - r1) / math.tan(angle2 / 2)
    return (
        wp.transformed(rotate=(0, -90, 0))
        .moveTo(t, 0)
        .line(-cone1_depth, r1)
        .lineTo(cone2_depth, r1)
        .lineTo(0, r2)
        .lineTo(0, 0)
        .close()
        .revolve(
            360,
            (0, 0, 0),
            (1, 0, 0),
            combine=False,
        )
    )


def d76b(
    wp: cityel_drive_axle_model.workplane.Workplane,
    axle_radius: float,
    thread_nominal_diameter: float,
) -> cityel_drive_axle_model.workplane.Workplane:
    """Return a DIN 76-B thread undercut.

    Reference: https://www.scribd.com/document/444544681/385876140-DIN-76-B-pdf .
    """
    # https://page-one.springer.com/pdf/preview/10.1007/978-3-322-92719-4_8
    # for 14-16mm diameter
    # measurements:
    #   https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#undercut-diameter
    #   https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#undercut-diameter-1
    dg = thread_nominal_diameter - 3
    rg = dg / 2
    # for 1.5mm pitch
    # measurements:
    #   https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#undercut-length
    #   https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#undercut-length-1
    g1 = 1.8
    g2 = 3.8
    r = 0.8

    wire = (
        wp.moveTo(g2, axle_radius)
        .lineTo(g2, thread_nominal_diameter / 2)
        # TODO: is this correct?
        .lineTo(g1, rg)
        .lineTo(0, rg)
    )
    fillet_vertices = wire.vertices().objects
    wire = wire.lineTo(0, axle_radius)
    rotation_edge = wire.val().Edges()[-1]
    wire = wire.close().val()
    wire = wire.fillet2D(
        r,
        wire.vertices(
            cq.selectors.SumSelector(
                *(
                    cq.selectors.NearestToPointSelector(v.toTuple())
                    for v in fillet_vertices
                )
            )
        ),
    )
    return (
        cityel_drive_axle_model.workplane.Workplane(obj=cq.Face.makeFromWires(wire))
        .rotate(
            *[v.toTuple() for v in rotation_edge.Vertices()],
            -90,
        )
        .revolve(
            axisStart=(0, 0, 0),
            axisEnd=wp.plane.zDir,
            combine=False,
        )
    )
