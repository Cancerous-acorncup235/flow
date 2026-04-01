"""Tests for visualization utilities."""

import numpy as np
import pytest
import tempfile
import os

from app.solvers.visualization import (
    interpolate_colormap,
    stress_to_colors,
    temperature_to_colors,
    compute_von_mises,
    displacement_to_vertex_positions,
    export_vtk,
    VIRIDIS,
    THERMAL,
)


class TestColormap:
    def test_viridis_min_is_purple(self):
        color = interpolate_colormap(0.0, VIRIDIS, 0.0, 1.0)
        assert color[0] > 0.2  # Red component
        assert color[2] > 0.3  # Blue component

    def test_viridis_max_is_yellow(self):
        color = interpolate_colormap(1.0, VIRIDIS, 0.0, 1.0)
        assert color[0] > 0.9  # High red
        assert color[1] > 0.8  # High green

    def test_thermal_min_is_blue(self):
        color = interpolate_colormap(0.0, THERMAL, 0.0, 1.0)
        assert color[2] > color[0]  # More blue than red

    def test_thermal_max_is_red(self):
        color = interpolate_colormap(1.0, THERMAL, 0.0, 1.0)
        assert color[0] > color[2]  # More red than blue

    def test_clamp_below_zero(self):
        color = interpolate_colormap(-1.0, VIRIDIS, 0.0, 1.0)
        # Should clamp to minimum
        assert all(0 <= c <= 1 for c in color)

    def test_clamp_above_one(self):
        color = interpolate_colormap(2.0, VIRIDIS, 0.0, 1.0)
        assert all(0 <= c <= 1 for c in color)


class TestStressToColors:
    def test_returns_correct_count(self):
        stress = np.array([10.0, 20.0, 30.0, 40.0])
        colors = stress_to_colors(stress)
        assert len(colors) == 4

    def test_colors_are_valid_rgb(self):
        stress = np.array([0.0, 100.0, 200.0])
        colors = stress_to_colors(stress)
        for c in colors:
            assert all(0 <= v <= 1 for v in c)


class TestTemperatureToColors:
    def test_returns_correct_shape(self):
        temp = np.random.rand(10, 10) * 100
        colors = temperature_to_colors(temp)
        assert colors.shape == (10, 10, 3)


class TestVonMises:
    def test_zero_stress_zero_vm(self):
        vm = compute_von_mises(
            np.array([0.0]),
            np.array([0.0]),
            np.array([0.0]),
        )
        assert vm[0] == pytest.approx(0.0)

    def test_uniaxial_stress(self):
        vm = compute_von_mises(
            np.array([100.0]),
            np.array([0.0]),
            np.array([0.0]),
        )
        assert vm[0] == pytest.approx(100.0)


class TestDisplacement:
    def test_zero_scale_no_change(self):
        nodes = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 1.0]])
        disp = np.array([[0.1, 0.0], [0.0, 0.2], [0.05, 0.05]])
        result = displacement_to_vertex_positions(nodes, disp, scale=0.0)
        assert np.allclose(result, nodes)

    def test_scale_applied(self):
        nodes = np.array([[0.0, 0.0]])
        disp = np.array([[1.0, 0.0]])
        result = displacement_to_vertex_positions(nodes, disp, scale=2.0)
        assert result[0, 0] == pytest.approx(2.0)


class TestVTKExport:
    def test_export_creates_file(self):
        nodes = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 1.0]])
        elements = np.array([[0, 1, 2]])
        point_data = {"stress": np.array([10.0, 20.0, 30.0])}

        with tempfile.NamedTemporaryFile(suffix=".vtk", delete=False) as f:
            filepath = f.name

        try:
            export_vtk(nodes, elements, point_data, filepath)
            assert os.path.exists(filepath)

            with open(filepath) as f:
                content = f.read()
            assert "POINTS 3" in content
            assert "CELLS 1" in content
            assert "SCALARS stress" in content
        finally:
            os.unlink(filepath)
