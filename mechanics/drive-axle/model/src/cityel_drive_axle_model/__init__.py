"""Models of the City-EL drive axles.

Based on a drawing @
https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/axle-drawing.pdf
"""

from collections.abc import Sequence

import cadquery as cq
import cq_warehouse.thread

import cityel_drive_axle_model.din
import cityel_drive_axle_model.keyway
import cityel_drive_axle_model.spline_cutter
import cityel_drive_axle_model.workplane


class Axle:
    """An axle without motor keyways."""

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#axle
    LENGTH = 1039.5
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#axle-diameter
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#axle-diameter-1
    DIAMETER = 25
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#diameter
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#diameter-2
    BEARING_DIAMETER = 20

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#diameter-1
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#diameter-3
    THREAD_NOMINAL_DIAMETER = 16
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#pitch
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#pitch-1
    THREAD_PITCH = 1.5

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#length
    CLUTCH_BEARING_REDUCTION_LENGTH = 106.5
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#length-1
    CLUTCH_THREAD_LENGTH = 20
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#width
    CLUTCH_KEY_LENGTH = 9
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#thickness
    CLUTCH_WRENCH_SIZE = 16

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#length-2
    FIXED_BEARING_REDUCTION_LENGTH = 100
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#length-4
    FIXED_THREAD_LENGTH = 24.5

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#inner-diameter-1
    SPLINE_INNER_DIAMETER = 16.3
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#straight-segment-length
    SPLINE_STRAIGHT_SEGMENT_LENGTH = 45.5

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/axle-drawing.html?page=1&x=31.8&y=33.6&w=3&h=4
    BEARING_REDUCTION_FILLET_RADIUS = 0.8
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#chamfer
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#chamfer-1
    CHAMFER_INNER_DIAMETER = 13.4

    KEYWAYS: Sequence[cityel_drive_axle_model.keyway.Keyway] = ()

    def __init__(self) -> None:
        """Calculate intermediate attributes."""
        self.radius = self.DIAMETER / 2
        self.bearing_radius = self.BEARING_DIAMETER / 2

    def _bearing_reduction(
        self,
        axle: cityel_drive_axle_model.workplane.Workplane,
        side: bool,
        length: float,
        thread_length: float,
    ) -> (
        cityel_drive_axle_model.workplane.Workplane,
        cityel_drive_axle_model.workplane.Workplane,
    ):
        # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/axle-drawing.html?page=1&x=68.7&y=34&w=3&h=4

        chamfer_outer_radius = (
            self.THREAD_NOMINAL_DIAMETER / 2
            # https://github.com/gumyr/cq_warehouse/issues/81#issuecomment-1537502988
            + 0.0001
        )
        wp = axle.faces(
            cq.DirectionMinMaxSelector(
                axle.plane.zDir,
                directionMax=side,
            )
        ).workplane(invert=True)
        chamfer_size = (self.THREAD_NOMINAL_DIAMETER - self.CHAMFER_INNER_DIAMETER) / 2
        chamfer = (
            wp.transformed(rotate=(90, 0, 0))
            .moveTo(chamfer_outer_radius, 0)
            .line(0, chamfer_size)
            .line(-chamfer_size, -chamfer_size)
            .close()
            .revolve(
                360,
                (0, 0, 0),
                (0, 1, 0),
                combine=False,
            )
        )
        reduction = (
            wp.circle(self.radius)
            .circle(self.bearing_radius)
            .extrude(
                length,
                combine=False,
            )
            .edges(cq.DirectionMinMaxSelector(wp.plane.zDir))
            .edges("%CIRCLE")
            .sort(lambda e: e.radius())
            .first()
            .fillet(self.BEARING_REDUCTION_FILLET_RADIUS)
        )
        centering = cityel_drive_axle_model.din.d332a5(wp)
        thread = self._thread_cutout(
            wp,
            thread_length,
        )
        return (
            reduction + thread + centering + chamfer,
            thread.onTop(),
        )

    def _thread_cutout(
        self,
        wp: cityel_drive_axle_model.workplane.Workplane,
        length: float,
    ) -> cityel_drive_axle_model.workplane.Workplane:
        thread = cq_warehouse.thread.IsoThread(
            self.THREAD_NOMINAL_DIAMETER,
            self.THREAD_PITCH,
            length,
        )
        cutout = wp.circle(self.bearing_radius).circle(thread.min_radius).extrude(
            length,
            combine=False,
        ) - cityel_drive_axle_model.workplane.Workplane(thread).reframe(wp)
        undercut = cityel_drive_axle_model.din.d76b(
            cutout.onTop(invert=True), self.radius, self.THREAD_NOMINAL_DIAMETER
        )
        return cutout + undercut

    def _spline_cutouts(
        self,
        wp: cityel_drive_axle_model.workplane.Workplane,
    ) -> cityel_drive_axle_model.workplane.Workplane:
        # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/spline-drawing.html&page=4&x=25&y=30&w=55&h=40

        inner_radius = self.SPLINE_INNER_DIAMETER / 2
        cut_count = 12
        cutout = cityel_drive_axle_model.spline_cutter.cutout(
            wp,
            self.SPLINE_STRAIGHT_SEGMENT_LENGTH,
        )
        cutout = cutout.translate(wp.plane.xDir * inner_radius)
        cutouts = cityel_drive_axle_model.workplane.Workplane(wp.plane)
        for _ in range(cut_count):
            cutouts.add(cutout)
            cutout = cutout.rotateAboutAxis(
                "Z",
                360 / cut_count,
            )
        return cutouts

    def _clutch_key(
        self,
        wp: cityel_drive_axle_model.workplane.Workplane,
    ) -> cityel_drive_axle_model.workplane.Workplane:
        # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/axle-drawing.html?page=1&x=20&y=38.7&w=4&h=8

        return (
            wp.moveTo(self.radius, self.CLUTCH_WRENCH_SIZE / 2)
            .line(0, self.radius)
            .line(-self.DIAMETER, 0)
            .line(0, -self.radius)
            .close()
            .mirrorX()
            .extrude(self.CLUTCH_KEY_LENGTH)
        )

    def _fixed_end(
        self,
        axle: cityel_drive_axle_model.workplane.Workplane,
    ) -> cityel_drive_axle_model.workplane.Workplane:
        # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/axle-drawing.html?page=1&x=64.5&y=36.3&w=26&h=15

        brearing_reduction, key_plane = self._bearing_reduction(
            axle,
            False,
            self.FIXED_BEARING_REDUCTION_LENGTH,
            self.FIXED_THREAD_LENGTH,
        )
        return brearing_reduction + self._spline_cutouts(key_plane)

    def _clutch_end(
        self,
        axle: cityel_drive_axle_model.workplane.Workplane,
    ) -> cityel_drive_axle_model.workplane.Workplane:
        # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/axle-drawing.html?page=1&x=13&y=35.5&w=26&h=15

        bearing_reduction, key_plane = self._bearing_reduction(
            axle,
            True,
            self.CLUTCH_BEARING_REDUCTION_LENGTH,
            self.CLUTCH_THREAD_LENGTH,
        )
        return bearing_reduction + self._clutch_key(key_plane)

    def build(
        self,
        wp: cityel_drive_axle_model.workplane.Workplane,
    ) -> cityel_drive_axle_model.workplane.Workplane:
        """Build the axle."""
        axle = wp.cylinder(self.LENGTH, self.radius)
        axle -= self._clutch_end(axle)
        axle -= self._fixed_end(axle)

        for keyway in self.KEYWAYS:
            axle = keyway.cut(axle, self.radius)

        return axle


class Thrige(Axle):
    """An axle that has a keyway for a Thrige Titan TTL 140B motor."""

    KEYWAYS = (cityel_drive_axle_model.keyway.Thrige,)


class Perm(Axle):
    """An axle that has a keyway for a Perm PMG132 motor."""

    KEYWAYS = (
        cityel_drive_axle_model.keyway.PermLeft,
        cityel_drive_axle_model.keyway.PermRight,
    )


class PermThrige(Axle):
    """An axle that has keyways for both Thrige and Perm motors."""

    KEYWAYS = Thrige.KEYWAYS + Perm.KEYWAYS
