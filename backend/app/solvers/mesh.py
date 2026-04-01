"""
Mesh Generation Utilities

Provides mesh generation for common geometries.
"""

import numpy as np
from dataclasses import dataclass


@dataclass
class Mesh2D:
    nodes: np.ndarray  # (N, 2) array of node coordinates
    elements: np.ndarray  # (E, 3) array of triangle node indices
    boundary_nodes: dict  # name -> list of node indices


def rectangular_mesh(
    width: float = 1.0,
    height: float = 1.0,
    nx: int = 10,
    ny: int = 10,
) -> Mesh2D:
    """Generate a 2D rectangular mesh with triangular elements."""
    # Generate node coordinates
    x = np.linspace(0, width, nx + 1)
    y = np.linspace(0, height, ny + 1)
    xx, yy = np.meshgrid(x, y)
    nodes = np.column_stack([xx.ravel(), yy.ravel()])

    # Generate elements (2 triangles per quad)
    elements = []
    for j in range(ny):
        for i in range(nx):
            n0 = j * (nx + 1) + i
            n1 = n0 + 1
            n2 = n0 + (nx + 1)
            n3 = n2 + 1
            elements.append([n0, n1, n2])
            elements.append([n1, n3, n2])

    # Identify boundary nodes
    boundary = {
        "left": [j * (nx + 1) for j in range(ny + 1)],
        "right": [j * (nx + 1) + nx for j in range(ny + 1)],
        "bottom": list(range(nx + 1)),
        "top": list(range(ny * (nx + 1), (ny + 1) * (nx + 1))),
    }

    return Mesh2D(nodes=nodes, elements=np.array(elements), boundary_nodes=boundary)


def circular_mesh(
    radius: float = 1.0,
    n_rings: int = 5,
    n_sectors: int = 16,
) -> Mesh2D:
    """Generate a 2D circular mesh."""
    nodes = [[0.0, 0.0]]  # Center node
    node_idx = 1
    ring_indices = [[0]]

    for ring in range(1, n_rings + 1):
        r = radius * ring / n_rings
        ring_start = node_idx
        ring_nodes = []
        for sector in range(n_sectors):
            theta = 2 * np.pi * sector / n_sectors
            nodes.append([r * np.cos(theta), r * np.sin(theta)])
            ring_nodes.append(node_idx)
            node_idx += 1
        ring_indices.append(ring_nodes)

    nodes = np.array(nodes)

    # Generate elements
    elements = []
    # Inner ring to center
    inner = ring_indices[1]
    for i in range(len(inner)):
        n0 = 0  # center
        n1 = inner[i]
        n2 = inner[(i + 1) % len(inner)]
        elements.append([n0, n1, n2])

    # Between rings
    for ring in range(1, n_rings):
        inner = ring_indices[ring]
        outer = ring_indices[ring + 1]
        for i in range(len(inner)):
            i0 = inner[i]
            i1 = inner[(i + 1) % len(inner)]
            o0 = outer[i]
            o1 = outer[(i + 1) % len(outer)]
            elements.append([i0, o0, i1])
            elements.append([i1, o0, o1])

    boundary = {
        "outer": ring_indices[-1],
        "center": [0],
    }

    return Mesh2D(nodes=nodes, elements=np.array(elements), boundary_nodes=boundary)


def l_mesh(
    size: float = 1.0,
    notch: float = 0.3,
    n: int = 10,
) -> Mesh2D:
    """Generate an L-shaped mesh (common benchmark geometry)."""
    # Create full rectangle mesh then remove the notch region
    mesh = rectangular_mesh(width=size, height=size, nx=n, ny=n)

    # Remove nodes and elements in the notch region
    mask = ~((mesh.nodes[:, 0] > size - notch) & (mesh.nodes[:, 1] > size - notch))
    keep_nodes = np.where(mask)[0]

    # Remap node indices
    node_map = {old: new for new, old in enumerate(keep_nodes)}
    new_nodes = mesh.nodes[keep_nodes]

    # Filter and remap elements
    new_elements = []
    for elem in mesh.elements:
        if all(n in node_map for n in elem):
            new_elements.append([node_map[n] for n in elem])

    return Mesh2D(
        nodes=new_nodes,
        elements=np.array(new_elements),
        boundary_nodes={"all": list(range(len(new_nodes)))},
    )
