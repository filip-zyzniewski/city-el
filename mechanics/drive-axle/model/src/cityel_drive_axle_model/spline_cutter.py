"""Model of the tool that can be used to cut spline grooves."""

# Based on the drawings @
#   https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.pdf

import cadquery as cq

import cityel_drive_axle_model.workplane


class Tool:
    """Represents a tool used to cut the spline grooves."""

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.html&page=2&x=38.5&y=83.5&w=8&h=4
    DIAMETER = 26
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.html&page=2&x=77&y=63&w=2.5&h=3
    THICKNESS = 4
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.html&page=2&x=73.9&y=59.5&w=2.5&h=8
    THICKNESS_AT_ARC = 3.266
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.html&page=2&x=71&y=59.6&w=2.5&h=8
    FACE_THICKNESS = 1.310
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.html&page=2&x=38.5&y=78.8&w=8&h=4
    ARC_START_DIAMETER = 22.67
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.html&page=2&x=38.5&y=74.5&w=8&h=4
    INNER_DIAMETER = 22.403
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.html&page=2&x=19&y=64&w=5&h=4
    TOOTH_SURFACE_RADIUS = 5.6
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.html&page=2&x=10.4&y=53.2&w=5&h=4
    CONVEX_FILLET_RADIUS = 0.5
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.html&page=2&x=20.5&y=60.4&w=5&h=4
    CONCAVE_FILLET_RADIUS = 0.3

    @classmethod
    def _wire(
        cls,
        wp: cityel_drive_axle_model.workplane.Workplane,
    ) -> (
        cq.Wire,
        (cq.Vertex, cq.Vertex),
    ):
        def first_vertex() -> cq.Vertex:
            return half.val().Vertices()[0]

        def last_vertex() -> cq.Vertex:
            return half.val().Vertices()[-1]

        arc_start_radius = cls.ARC_START_DIAMETER / 2
        radius = cls.DIAMETER / 2
        inner_radius = cls.INNER_DIAMETER / 2

        half = wp.moveTo(0, 0).lineTo(0, cls.FACE_THICKNESS / 2)
        mirror_edge_start = first_vertex()
        convex_vertex = last_vertex()
        half = half.radiusArc(
            (
                radius - arc_start_radius,
                cls.THICKNESS_AT_ARC / 2,
            ),
            -cls.TOOTH_SURFACE_RADIUS,
        )
        concave_vertex = last_vertex()

        half = (
            half.lineTo(
                radius - inner_radius,
                cls.THICKNESS / 2,
            )
            .lineTo(
                radius,
                cls.THICKNESS / 2,
            )
            .lineTo(
                radius,
                0,
            )
        )
        axis = (
            half.val().Vertices()[-2],
            last_vertex(),
        )

        mirror_edge_end = last_vertex()

        half = half.wire().val()
        for r, v in (
            (cls.CONVEX_FILLET_RADIUS, convex_vertex),
            (cls.CONCAVE_FILLET_RADIUS, concave_vertex),
        ):
            half = half.fillet2D(
                r,
                [half.vertices(cq.selectors.NearestToPointSelector(v.toTuple()))],
            )

        second_half = half.rotate(
            mirror_edge_start.toTuple(),
            mirror_edge_end.toTuple(),
            180,
        )

        return (half.stitch(second_half), axis)

    @classmethod
    def face(
        cls,
        wp: cityel_drive_axle_model.workplane.Workplane,
    ) -> cq.Face:
        """Build a cadquery face of the cutting tool."""
        wire, axis = cls._wire(wp)
        return cq.Face.makeFromWires(wire), axis

    @classmethod
    def build(
        cls,
        wp: cityel_drive_axle_model.workplane.Workplane,
    ) -> cityel_drive_axle_model.workplane.Workplane:
        """Build the tool."""
        face, axis = cls.face(wp)
        return wp.add(face).revolve(
            180,
            *[wp.plane.toLocalCoords(v).toTuple() for v in axis],
        )


def cutout(
    wp: cityel_drive_axle_model.workplane.Workplane,
    straight_length: float,
) -> cityel_drive_axle_model.workplane.Workplane:
    """Build a shape that would be cut out by a moving cutter."""
    face, axis = Tool.face(wp)
    straight = wp.add(face).extrude(straight_length)
    tool = Tool.build(straight.onTop(invert=True))
    return straight.union(tool)
