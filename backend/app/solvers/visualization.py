"""
Result Visualization Utilities

Converts simulation results to formats suitable for 3D rendering.
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class ColorMap:
    name: str
    colors: list[tuple[float, float, float]]  # RGB 0-1

# Built-in colormaps
VIRIDIS = ColorMap("viridis", [
    (0.267, 0.004, 0.329),
    (0.282, 0.140, 0.458),
    (0.253, 0.265, 0.530),
    (0.206, 0.372, 0.553),
    (0.163, 0.471, 0.558),
    (0.128, 0.567, 0.551),
    (0.135, 0.659, 0.518),
    (0.267, 0.749, 0.441),
    (0.478, 0.821, 0.318),
    (0.741, 0.873, 0.150),
    (0.993, 0.906, 0.144),
])

THERMAL = ColorMap("thermal", [
    (0.0, 0.0, 0.5),   # Dark blue
    (0.0, 0.0, 1.0),   # Blue
    (0.0, 1.0, 1.0),   # Cyan
    (0.0, 1.0, 0.0),   # Green
    (1.0, 1.0, 0.0),   # Yellow
    (1.0, 0.5, 0.0),   # Orange
    (1.0, 0.0, 0.0),   # Red
])


def interpolate_colormap(value: float, colormap: ColorMap, vmin: float = 0.0, vmax: float = 1.0) -> tuple[float, float, float]:
    """Map a scalar value to RGB color using a colormap."""
    # Normalize to 0-1
    t = (value - vmin) / (vmax - vmin + 1e-10)
    t = max(0.0, min(1.0, t))

    # Find position in colormap
    n = len(colormap.colors)
    idx = t * (n - 1)
    i = int(idx)
    f = idx - i

    if i >= n - 1:
        return colormap.colors[-1]

    c0 = colormap.colors[i]
    c1 = colormap.colors[i + 1]

    return (
        c0[0] + f * (c1[0] - c0[0]),
        c0[1] + f * (c1[1] - c0[1]),
        c0[2] + f * (c1[2] - c0[2]),
    )


def stress_to_colors(
    stress: np.ndarray,
    colormap: ColorMap = VIRIDIS,
) -> list[tuple[float, float, float]]:
    """Convert stress array to colors for visualization."""
    vmin = float(np.min(stress))
    vmax = float(np.max(stress))

    colors = []
    for val in stress.flat:
        colors.append(interpolate_colormap(float(val), colormap, vmin, vmax))

    return colors


def temperature_to_colors(
    temperature: np.ndarray,
    colormap: ColorMap = THERMAL,
) -> np.ndarray:
    """Convert temperature field to RGB color array."""
    vmin = float(np.min(temperature))
    vmax = float(np.max(temperature))

    h, w = temperature.shape
    colors = np.zeros((h, w, 3))

    for i in range(h):
        for j in range(w):
            colors[i, j] = interpolate_colormap(temperature[i, j], colormap, vmin, vmax)

    return colors


def displacement_to_vertex_positions(
    nodes: np.ndarray,
    displacements: np.ndarray,
    scale: float = 1.0,
) -> np.ndarray:
    """Scale displacements and add to node positions for deformed shape."""
    return nodes + scale * displacements


def compute_von_mises(
    sigma_xx: np.ndarray,
    sigma_yy: np.ndarray,
    tau_xy: np.ndarray,
) -> np.ndarray:
    """Compute von Mises stress from stress components."""
    return np.sqrt(sigma_xx**2 - sigma_xx * sigma_yy + sigma_yy**2 + 3 * tau_xy**2)


def export_vtk(
    nodes: np.ndarray,
    elements: np.ndarray,
    point_data: dict[str, np.ndarray],
    filepath: str,
):
    """Export mesh and results to VTK format for ParaView."""
    with open(filepath, 'w') as f:
        f.write("# vtk DataFile Version 3.0\n")
        f.write("FLOW Simulation Results\n")
        f.write("ASCII\n")
        f.write("DATASET UNSTRUCTURED_GRID\n")

        n_nodes = len(nodes)
        n_elements = len(elements)

        # Points
        f.write(f"POINTS {n_nodes} float\n")
        for node in nodes:
            if len(node) == 2:
                f.write(f"{node[0]} {node[1]} 0.0\n")
            else:
                f.write(f"{node[0]} {node[1]} {node[2]}\n")

        # Cells
        f.write(f"CELLS {n_elements} {n_elements * (elements.shape[1] + 1)}\n")
        for elem in elements:
            f.write(f"{len(elem)} {' '.join(str(n) for n in elem)}\n")

        # Cell types (all triangles)
        f.write(f"CELL_TYPES {n_elements}\n")
        for _ in range(n_elements):
            f.write("5\n")  # VTK_TRIANGLE

        # Point data
        if point_data:
            f.write(f"POINT_DATA {n_nodes}\n")
            for name, data in point_data.items():
                if data.ndim == 1:
                    f.write(f"SCALARS {name} float 1\n")
                    f.write("LOOKUP_TABLE default\n")
                    for val in data:
                        f.write(f"{val}\n")
                elif data.ndim == 2 and data.shape[1] == 2:
                    f.write(f"VECTORS {name} float\n")
                    for row in data:
                        f.write(f"{row[0]} {row[1]} 0.0\n")
