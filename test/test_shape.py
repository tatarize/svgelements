from __future__ import print_function

import unittest

from svgelements import *


class TestElementShape(unittest.TestCase):

    def test_rect_dict(self):
        values = {
            'tag': 'rect',
            'rx': "4",
            'ry': "2",
            'x': "50",
            'y': "51",
            'width': "20",
            'height': "10"
        }
        e = Rect(values)
        e2 = Rect(50, 51, 20, 10, 4, 2)
        self.assertEqual(e, e2)
        e2 *= "translate(2)"
        e3 = Rect()
        self.assertNotEqual(e, e3)

    def test_line_dict(self):
        values = {
            'tag': 'rect',
            'x1': "0",
            'y1': "0",
            'x2': "100",
            'y2': "100"
        }
        e = SimpleLine(values)
        e2 = SimpleLine(0, '0px', '100px', '100px')
        e3 = SimpleLine(0, 0, 100, 100)
        self.assertEqual(e, e2)
        self.assertEqual(e, e3)
        e4 = SimpleLine()
        self.assertNotEqual(e, e4)

    def test_ellipse_dict(self):
        values = {
            'tag': 'ellipse',
            'rx': "4.0",
            'ry': "8.0",
            'cx': "22.4",
            'cy': "33.33"
        }
        e = Ellipse(values)
        e2 = Ellipse(22.4, 33.33, 4, 8)
        self.assertEqual(e, e2)
        e3 = Ellipse()
        self.assertNotEqual(e, e3)

    def test_circle_dict(self):
        values = {
            'tag': 'circle',
            'r': "4.0",
            'cx': "22.4",
            'cy': "33.33"
        }
        e = Circle(values)
        e2 = Circle(22.4, 33.33, 4)
        self.assertEqual(e, e2)
        e3 = Circle()
        self.assertNotEqual(e, e3)
        circle_d = e.d()
        self.assertEqual(Path(circle_d),
                         'M26.4,33.33A4,4 0 0,1 22.4,37.33 A4,4 0 0,1 18.4,33.33 A4,4 0 0,1 22.4,29.33 A4,4 0 0,1 26.4,33.33Z')

    def test_polyline_dict(self):
        values = {
            'tag': 'polyline',
            'points': '0,100 50,25 50,75 100,0',
        }
        e = Polyline(values)
        e2 = Polyline(0, 100, 50, 25, 50, 75, 100, 0)
        self.assertEqual(e, e2)
        e3 = Polyline()
        self.assertNotEqual(e, e3)
        polyline_d = e.d()
        self.assertEqual(Path(polyline_d), "M 0,100 L 50,25 L 50,75 L 100,0")

    def test_polygon_dict(self):
        values = {
            'tag': 'polyline',
            'points': '0,100 50,25 50,75 100,0',
        }
        e = Polygon(values)
        e2 = Polygon(0, 100, 50, 25, 50, 75, 100, 0)
        self.assertEqual(e, e2)
        e3 = Polygon()
        self.assertNotEqual(e, e3)
        polygon_d = e.d()
        self.assertEqual(Path(polygon_d), 'M 0,100 L 50,25 L 50,75 L 100,0 Z')

    def test_circle_ellipse_equal(self):
        self.assertTrue(Ellipse(center=(0, 0), rx=10, ry=10) == Circle(center="0,0", r=10.0))

    def test_transform_circle_to_ellipse(self):
        c = Circle(center="0,0", r=10.0)
        p = c * Matrix.skew_x(Angle.degrees(50))
        p.reify()
        p = c * "translate(10,1)"
        p.reify()
        p = c * "scale(10,1)"
        p.reify()
        p = c * "rotate(10deg)"
        p.reify()
        p = c * "skewy(10)"
        p.reify()
        self.assertFalse(isinstance(Circle(), Ellipse))
        self.assertFalse(isinstance(Ellipse(), Circle))

    def test_circle_decomp(self):
        circle = Circle()
        c = Path(circle.d())
        self.assertEqual(c, "M 1,0 A 1,1 0 0,1 0,1 A 1,1 0 0,1 -1,0 A 1,1 0 0,1 0,-1 A 1,1 0 0,1 1,0 Z")
        circle *= "scale(2,1)"
        c = Path(circle.d())
        self.assertEqual(c, "M 2,0 A 2,1 0 0,1 0,1 A 2,1 0 0,1 -2,0 A 2,1 0 0,1 0,-1 A 2,1 0 0,1 2,0 Z")
        circle *= "scale(0.5,1)"
        c = Path(circle.d())
        self.assertEqual(c, "M 1,0 A 1,1 0 0,1 0,1 A 1,1 0 0,1 -1,0 A 1,1 0 0,1 0,-1 A 1,1 0 0,1 1,0 Z")

    def test_circle_implicit(self):
        shape = Circle()
        shape *= "translate(40,40) rotate(15deg) scale(2,1.5)"
        self.assertAlmostEqual(shape.implicit_rx, 2.0)
        self.assertAlmostEqual(shape.implicit_ry, 1.5)
        self.assertAlmostEqual(shape.rotation, Angle.degrees(15))
        self.assertEqual(shape.implicit_center, (40, 40))

    def test_rect_implicit(self):
        shape = Rect()
        shape *= "translate(40,40) rotate(15deg) scale(2,1.5)"
        self.assertAlmostEqual(shape.implicit_x, 40)
        self.assertAlmostEqual(shape.implicit_y, 40)
        self.assertAlmostEqual(shape.implicit_width, 2)
        self.assertAlmostEqual(shape.implicit_height, 1.5)
        self.assertAlmostEqual(shape.implicit_rx, 0)
        self.assertAlmostEqual(shape.implicit_ry, 0)
        self.assertAlmostEqual(shape.rotation, Angle.degrees(15))

    def test_line_implicit(self):
        shape = SimpleLine(0, 0, 1, 1)
        shape *= "translate(40,40) rotate(15deg) scale(2,1.5)"
        self.assertAlmostEqual(shape.implicit_x1, 40)
        self.assertAlmostEqual(shape.implicit_y1, 40)
        p = Point(1, 1) * "rotate(15deg) scale(2,1.5)"
        self.assertAlmostEqual(shape.implicit_x2, 40 + p[0])
        self.assertAlmostEqual(shape.implicit_y2, 40 + p[1])
        self.assertAlmostEqual(shape.rotation, Angle.degrees(15))

    def test_circle_equals_transformed_circle(self):
        shape1 = Circle(r=2)
        shape2 = Circle() * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_rect_equals_transformed_rect(self):
        shape1 = Rect(x=0, y=0, width=2, height=2)
        shape2 = Rect(0, 0, 1, 1) * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_rrect_equals_transformed_rrect(self):
        shape1 = Rect(0, 0, 2, 2, 1, 1)
        shape2 = Rect(0, 0, 1, 1, 0.5, 0.5) * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_line_equals_transformed_line(self):
        shape1 = SimpleLine(0, 0, 2, 2)
        shape2 = SimpleLine(0, 0, 1, 1) * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_polyline_equals_transformed_polyline(self):
        shape1 = Polyline(0, 0, 2, 2)
        shape2 = Polyline(0, 0, 1, 1) * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_polygon_equals_transformed_polygon(self):
        shape1 = Polyline(0, 0, 2, 2)
        shape2 = Polyline(0, 0, 1, 1) * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_polyline_not_equal_transformed_polygon(self):
        shape1 = Polyline(0, 0, 2, 2)
        shape2 = Polygon(0, 0, 1, 1) * "scale(2)"
        self.assertNotEqual(shape1, shape2)

    def test_polyline_closed_equals_transformed_polygon(self):
        shape1 = Path(Polyline(0, 0, 2, 2)) + "z"
        shape2 = Polygon(0, 0, 1, 1) * "scale(2)"
        self.assertEqual(shape1, shape2)

    def test_path_plus_shape(self):
        path = Path("M 0,0 z")
        path += Rect(0, 0, 1, 1)
        self.assertEqual(path, "M0,0zM0,0h1v1h-1z")

    def test_circle_not_equal_red_circle(self):
        shape1 = Circle()
        shape2 = Circle(stroke="red")
        self.assertNotEqual(shape1, shape2)
        shape1 = Circle()
        shape2 = Circle(fill="red")
        self.assertNotEqual(shape1, shape2)

    def test_rect_initialize(self):
        shapes = (
            Rect(),
            Rect(0),
            Rect(0, 0),
            Rect(0, 0, 1),
            Rect(0, 0, 1, 1),
            Rect(0, y=0),
            Rect(0, y=0, width=1),
            Rect(0, y=0, width=1, height=1),
            Rect(width=1, height=1, x=0, y=0),
            Rect(0, 0, 1, 1, 0, 0),
            Rect(0, 0, 1, 1, rx=0, ry=0)
        )
        for s in shapes:
            self.assertEqual(shapes[0], s)

    def test_circle_initialize(self):
        shapes = (
            Circle(),
            Circle(0, 0),
            Circle(center=(0, 0), r=1),
            Circle("0px", "0px", 1),
            Ellipse("0", "0", 1, 1),
            Ellipse("0", "0", rx=1, ry=1),
            Ellipse(0, 0, 1, ry=1),
            Circle(Circle()),
            Circle({"cx": 0, "cy": 0, "r": 1}),
            Ellipse({"cx": 0, "cy": 0, "rx": 1}),
            Ellipse({"cx": 0, "cy": 0, "ry": 1}),
            Ellipse({"cx": 0, "cy": 0, "rx": 1, "ry": 1.0}),
            Circle(Ellipse()),
            Ellipse(Circle())
        )
        for s in shapes:
            self.assertEqual(shapes[0], s)

    def test_polyline_initialize(self):
        shapes = (
            Polyline(0, 0, 1, 1),
            Polyline((0, 0), (1, 1)),
            Polyline(points=((0, 0), (1, 1))),
            Polyline("0,0", "1,1"),
            Polyline("0,0", (1, 1)),
            Polyline("0,0", Point(1, 1)),
            Polyline({"points": "0,0,1,1"}),
            Polyline(Polyline(0, 0, 1, 1)),
            Path("M0,0L1,1"),
            SimpleLine(0, 0, 1, 1),
        )
        for s in shapes:
            self.assertEqual(shapes[0], s)

    def test_polygon_initialize(self):
        shapes = (
            Polygon(0, 0, 1, 1),
            Polygon((0, 0), (1, 1)),
            Polygon(points=((0, 0), (1, 1))),
            Polygon("0,0", "1,1"),
            Polygon("0,0", (1, 1)),
            Polygon("0,0", Point(1, 1)),
            Polygon({"points": "0,0,1,1"}),
            Polygon(Polyline(0, 0, 1, 1)),
            Polygon("0,0,1,1"),
            Path("M0,0L1,1z"),
        )
        for s in shapes:
            self.assertEqual(shapes[0], s)

    def test_shapes_repr(self):
        s = Rect(fill='red')
        self.assertEqual(repr(s), "Rect(width=1, height=1, fill='#ff0000')")
        s = Ellipse(fill='red')
        self.assertEqual(repr(s), "Ellipse(cx=0, cy=0, r=1, fill='#ff0000')")
        s = Circle(fill='red')
        self.assertEqual(repr(s), "Circle(cx=0, cy=0, r=1, fill='#ff0000')")
        s = SimpleLine(fill='red')
        self.assertEqual(repr(s), "SimpleLine(x1=0.0, y1=0.0, x2=0.0, y2=0.0, fill='#ff0000')")
        s = Polygon(fill='red')
        self.assertEqual(repr(s), "Polygon(points=(''), fill='#ff0000')")
        s = Polyline(fill='red')
        self.assertEqual(repr(s), "Polyline(points=(''), fill='#ff0000')")
        s = Path(fill='red')
        self.assertEqual(repr(s), "Path(fill='#ff0000')")

    def test_shape_bbox(self):
        s = Rect() * 'scale(20)'
        self.assertEqual(s.bbox(False), (0, 0, 1, 1))
        self.assertEqual(s.bbox(True), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(False), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(True), (0, 0, 1, 1))
        s = Circle() * 'scale(20)'
        self.assertEqual(s.bbox(False), (-1, -1, 1, 1))
        self.assertEqual(s.bbox(True), (-20, -20, 20, 20))
        self.assertNotEqual(s.bbox(False), (-20, -20, 20, 20))
        self.assertNotEqual(s.bbox(True), (-1, -1, 1, 1))
        s = Ellipse() * 'scale(20)'
        self.assertEqual(s.bbox(False), (-1, -1, 1, 1))
        self.assertEqual(s.bbox(True), (-20, -20, 20, 20))
        self.assertNotEqual(s.bbox(False), (-20, -20, 20, 20))
        self.assertNotEqual(s.bbox(True), (-1, -1, 1, 1))
        s = Polygon() * 'scale(20)'
        self.assertEqual(s.bbox(False), None)
        self.assertEqual(s.bbox(True), None)
        self.assertNotEqual(s.bbox(False), (0, 0, 0, 0))
        self.assertNotEqual(s.bbox(True), (0, 0, 0, 0))
        s = Polyline() * 'scale(20)'
        self.assertEqual(s.bbox(False), None)
        self.assertEqual(s.bbox(True), None)
        self.assertNotEqual(s.bbox(False), (0, 0, 0, 0))
        self.assertNotEqual(s.bbox(True), (0, 0, 0, 0))
        s = Polygon("0,0 0,1 1,1 1,0 0,0") * 'scale(20)'
        self.assertEqual(s.bbox(False), (0, 0, 1, 1))
        self.assertEqual(s.bbox(True), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(False), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(True), (0, 0, 1, 1))
        s = Polyline("0,0 0,1 1,1 1,0 0,0") * 'scale(20)'
        self.assertEqual(s.bbox(False), (0, 0, 1, 1))
        self.assertEqual(s.bbox(True), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(False), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(True), (0, 0, 1, 1))
        s = SimpleLine(0, 0, 1, 1) * 'scale(20)'
        self.assertEqual(s.bbox(False), (0, 0, 1, 1))
        self.assertEqual(s.bbox(True), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(False), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(True), (0, 0, 1, 1))

    def test_rect_rot_equal_rect_path_rotate(self):
        r = Rect(10, 10, 8, 4)
        a = r.d()
        b = Path(a).d()
        self.assertEqual(a, b)
        a = (Path(r.d()) * "rotate(0.5turns)").d()
        b = (r * "rotate(0.5turns)").d()
        self.assertEqual(a, b)

    def test_rect_reify(self):
        """Reifying a rotated rect."""
        test_reification(self, Rect())
        test_reification(self, Rect(2, 2, 4, 4))

        shape = Rect() * "rotate(-90) translate(20,0)"
        t = Rect(0, -20, 1, 1)
        t *= "rotate(-90, 0, -20)"
        self.assertEqual(t, shape)

    def test_circle_reify(self):
        """Reifying a rotated circle."""
        test_reification(self, Circle())
        test_reification(self, Circle(2, 2, 4, 4))

    def test_ellipse_reify(self):
        """Reifying a rotated ellipse."""
        test_reification(self, Ellipse(rx=1, ry=2))
        test_reification(self, Ellipse(2, 2, 5, 8))

    def test_polyline_reify(self):
        """Reifying a rotated polyline."""
        test_reification(self, Polyline("0,0 1,1 2,2"))
        test_reification(self, Polyline("0,0 1,1 2,0"))

    def test_polygon_reify(self):
        """Reifying a rotated polygon."""
        test_reification(self, Polygon("0,0 1,1 2,2"))
        test_reification(self, Polygon("0,0 1,1 2,0"))

    def test_line_reify(self):
        """Reifying a rotated line."""
        test_reification(self, SimpleLine(0, 0, 1, 1))
        test_reification(self, SimpleLine(2, 2, 1, 0))

    def test_path_reify(self):
        """Reifying a path."""
        test_reification(self, Path("M0,0L1,1L1,0z"))
        test_reification(self, Path("M100,100L70,70L45,0z"))


def test_reification(test, shape):
    correct_reify(test, shape * "rotate(-90) translate(20,0)")
    correct_reify(test, shape * "rotate(12turn)")
    correct_reify(test, shape * "translate(20,0)")
    correct_reify(test, shape * "scale(2) translate(20,0)")
    correct_reify(test, shape * "rotate(90) scale(-1) translate(20,0)")
    correct_reify(test, shape * "rotate(90) translate(20,0)")
    correct_reify(test, shape * "skewX(10)")
    correct_reify(test, shape * "skewY(10)")


def correct_reify(test, shape):
    path = abs(Path(shape))
    reified = abs(copy(shape))
    test.assertEqual(path, shape)
    test.assertEqual(reified, shape)
    test.assertEqual(reified, path)
