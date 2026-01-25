"""Provides a subclass of cadquery.Workplane with extra features."""

import cadquery as cq


class Workplane(cq.Workplane):
    """Like `cq.Workplane`, but with some extra methods."""

    def onTop(self, invert: bool = False) -> "Workplane":
        """Return a new workplane on the face farthest in the zDir direction.

        The new workplane shares the xDir and the
        zDir (inverted if requested) with self.
        """
        z = self.plane.zDir
        origin = self.plane.origin
        face = self.faces(cq.DirectionMinMaxSelector(z)).val()

        offset = (face.Center() - origin).dot(z)

        # why not:
        # return plane.workplane(offset=offset, invert=invert)
        return type(self)(
            cq.Plane(
                origin + offset * z,
                self.plane.xDir,
                -z if invert else z,
            ),
        )

    def reframe(self, to: "Workplane") -> "Workplane":
        """Reframe objects from self onto another Workplane."""
        t = to.plane.rG.multiply(self.plane.rG.inverse())
        return to.newObject(o.transformShape(t) for o in self.objects)

    def rotateAboutAxis(self, axis: str, angleDegrees: float = 90) -> "Workplane":
        """Rotate the Workplane along the X, Y or Z axis."""
        origin = self.plane.origin
        return self.rotate(
            origin,
            origin + getattr(self.plane, axis.lower() + "Dir"),
            angleDegrees,
        )
