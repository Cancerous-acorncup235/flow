"""Tests for geometry parsers."""

import numpy as np
import pytest
import tempfile
import os

from app.solvers.geometry import (
    generate_box,
    generate_sphere,
    parse_obj,
    Geometry,
)


class TestBox:
    def test_has_8_vertices(self):
        box = generate_box()
        assert box.n_vertices == 8

    def test_has_12_faces(self):
        box = generate_box()
        assert box.n_faces == 12

    def test_bounds(self):
        box = generate_box(width=2, height=3, depth=4)
        lo, hi = box.bounds
        assert np.allclose(lo, [-1, -1.5, -2])
        assert np.allclose(hi, [1, 1.5, 2])

    def test_center(self):
        box = generate_box()
        assert np.allclose(box.center, [0, 0, 0])

    def test_extent(self):
        box = generate_box(width=2, height=4, depth=6)
        assert np.allclose(box.extent, [2, 4, 6])


class TestSphere:
    def test_center_at_origin(self):
        sphere = generate_sphere(radius=5.0)
        assert np.allclose(sphere.center, [0, 0, 0], atol=0.1)

    def test_radius(self):
        r = 3.0
        sphere = generate_sphere(radius=r)
        distances = np.linalg.norm(sphere.vertices, axis=1)
        assert np.allclose(distances, r, atol=0.1)


class TestOBJParser:
    def test_parse_simple_obj(self):
        obj_content = """v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 0.5 1.0 0.0
f 1 2 3
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.obj', delete=False) as f:
            f.write(obj_content)
            filepath = f.name

        try:
            geom = parse_obj(filepath)
            assert geom.n_vertices == 3
            assert geom.n_faces == 1
            assert geom.format == 'obj'
        finally:
            os.unlink(filepath)
