"""Models of the City-EL drive axles' motor keyways."""

import abc

import cadquery as cq

import cityel_drive_axle_model.workplane


class Keyway(abc.ABC):
    """An abstract axle keyway."""

    WIDTH: float
    HEIGHT: float
    DEPTH: float
    OFFSET: float

    @classmethod
    def cut(
        cls,
        axle: cityel_drive_axle_model.workplane.Workplane,
        axle_radius: float,
    ) -> cityel_drive_axle_model.workplane.Workplane:
        """Cut the keyway from the axle."""
        wp = axle.faces(
            cq.DirectionMinMaxSelector(
                axle.plane.zDir,
                directionMax=False,
            )
        ).workplane(invert=True)
        straight_width = cls.WIDTH - cls.HEIGHT
        radius = cls.HEIGHT / 2
        keyway = (
            wp.moveTo(0, radius)
            .line(
                straight_width / 2,
                0,
            )
            .radiusArc(
                (cls.WIDTH / 2, 0),
                radius,
            )
            .mirrorX()
            .mirrorY()
            .extrude(
                cls.DEPTH,
                combine=False,
            )
            .rotateAboutAxis("X", -90)
            .rotateAboutAxis("Y")
            .translate(
                (cls.OFFSET + cls.WIDTH / 2) * wp.plane.zDir
                - axle_radius * wp.plane.yDir
            )
        )
        return axle - keyway


class Thrige(Keyway):
    """Axle keyway for the Thrige Titan TTL 140B motor."""

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/axle-drawing.html?page=1&x=40&y=40.5&w=12&h=6

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#width-1
    WIDTH = 45
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#height-1
    HEIGHT = 8
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#depth
    DEPTH = 4
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/axle-drawing.html?page=1&x=70.3&y=16.6&w=5&h=3
    OFFSET = 359.5


class PermLeft(Keyway):
    """Left axle keyway for the Perm PMG132 motor."""

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/axle-drawing.html?page=1&x=53.2&y=41.7&w=9&h=4

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#width-2
    WIDTH = 22
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#height-2
    HEIGHT = 6
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#depth-1
    DEPTH = 4.5
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/axle-drawing.html?page=1&x=74.2&y=19.8&w=5&h=3
    OFFSET = 159.5


class PermRight(Keyway):
    """Right axle keyway for the Perm PMG132 motor."""

    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#width-3
    WIDTH = 36
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#height-3
    HEIGHT = 6
    # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#depth-2
    DEPTH = 4.5
    OFFSET = (
        PermLeft.OFFSET
        + PermLeft.WIDTH
        # https://filip-zyzniewski.github.io/city-el/mechanics/drive-axle/doc/dimensions/#perm
        + 123.6
    )
