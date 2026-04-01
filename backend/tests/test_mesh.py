"""Tests for mesh generation utilities."""

import numpy as np
import pytest

from app.solvers.mesh import rectangular_mesh, circular_mesh, l_mesh


class TestRectangularMesh:
    def test_node_count(self):
        mesh = rectangular_mesh(width=1.0, height=1.0, nx=10, ny=10)
        assert len(mesh.nodes) == 11 * 11

    def test_element_count(self):
        mesh = rectangular_mesh(nx=5, ny=5)
        assert len(mesh.elements) == 5 * 5 * 2

    def test_nodes_within_bounds(self):
        mesh = rectangular_mesh(width=2.0, height=0.5, nx=10, ny=5)
        assert np.all(mesh.nodes[:, 0] >= 0)
        assert np.all(mesh.nodes[:, 0] <= 2.0)
        assert np.all(mesh.nodes[:, 1] >= 0)
        assert np.all(mesh.nodes[:, 1] <= 0.5)

    def test_boundary_nodes(self):
        mesh = rectangular_mesh(nx=5, ny=3)
        assert len(mesh.boundary_nodes["left"]) == 4
        assert len(mesh.boundary_nodes["right"]) == 4
        assert len(mesh.boundary_nodes["bottom"]) == 6
        assert len(mesh.boundary_nodes["top"]) == 6


class TestCircularMesh:
    def test_center_node_exists(self):
        mesh = circular_mesh(radius=1.0, n_rings=3, n_sectors=8)
        assert np.allclose(mesh.nodes[0], [0, 0])

    def test_outer_nodes_on_circle(self):
        mesh = circular_mesh(radius=2.0, n_rings=3, n_sectors=16)
        outer = mesh.boundary_nodes["outer"]
        for idx in outer:
            r = np.linalg.norm(mesh.nodes[idx])
            assert abs(r - 2.0) < 0.01

    def test_element_count(self):
        mesh = circular_mesh(n_rings=2, n_sectors=8)
        # Inner ring: 8 triangles to center
        # Between rings: 8 * 2 = 16 triangles
        assert len(mesh.elements) == 8 + 16


class TestLMesh:
    def test_fewer_nodes_than_rectangle(self):
        rect = rectangular_mesh(size=1.0, nx=10, ny=10)
        l = l_mesh(size=1.0, notch=0.3, n=10)
        assert len(l.nodes) < len(rect.nodes)

    def test_elements_valid(self):
        mesh = l_mesh(size=1.0, notch=0.3, n=5)
        n_nodes = len(mesh.nodes)
        for elem in mesh.elements:
            for node_id in elem:
                assert 0 <= node_id < n_nodes
