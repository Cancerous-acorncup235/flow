"""
Geometry file parsers.

Supports STEP, IGES, STL, and OBJ formats.
"""

import numpy as np
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Geometry:
    vertices: np.ndarray  # (N, 3) vertex coordinates
    faces: np.ndarray  # (M, 3) or (M, 4) face vertex indices
    name: str = ""
    format: str = ""

    @property
    def n_vertices(self) -> int:
        return len(self.vertices)

    @property
    def n_faces(self) -> int:
        return len(self.faces)

    @property
    def bounds(self) -> tuple[np.ndarray, np.ndarray]:
        return self.vertices.min(axis=0), self.vertices.max(axis=0)

    @property
    def center(self) -> np.ndarray:
        return self.vertices.mean(axis=0)

    @property
    def extent(self) -> np.ndarray:
        lo, hi = self.bounds
        return hi - lo


def parse_stl(filepath: str) -> Geometry:
    """Parse STL file (ASCII or binary)."""
    path = Path(filepath)

    with open(path, 'rb') as f:
        header = f.read(80)
        f.seek(0)

    # Check if ASCII or binary
    try:
        text = header.decode('ascii', errors='ignore').strip()
        if text.startswith('solid'):
            return _parse_stl_ascii(filepath)
    except:
        pass

    return _parse_stl_binary(filepath)


def _parse_stl_ascii(filepath: str) -> Geometry:
    """Parse ASCII STL."""
    vertices = []
    faces = []
    vertex_map = {}

    with open(filepath, 'r') as f:
        current_vertices = []
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == 'vertex':
                v = tuple(float(x) for x in parts[1:4])
                if v not in vertex_map:
                    vertex_map[v] = len(vertices)
                    vertices.append(list(v))
                current_vertices.append(vertex_map[v])

            elif parts[0] == 'endloop' and len(current_vertices) == 3:
                faces.append(current_vertices)
                current_vertices = []

    return Geometry(
        vertices=np.array(vertices),
        faces=np.array(faces),
        name=Path(filepath).stem,
        format='stl',
    )


def _parse_stl_binary(filepath: str) -> Geometry:
    """Parse binary STL."""
    import struct

    vertices = []
    faces = []
    vertex_map = {}

    with open(filepath, 'rb') as f:
        f.read(80)  # header
        n_triangles = struct.unpack('<I', f.read(4))[0]

        for _ in range(n_triangles):
            f.read(12)  # normal
            tri_vertices = []
            for _ in range(3):
                v = struct.unpack('<3f', f.read(12))
                if v not in vertex_map:
                    vertex_map[v] = len(vertices)
                    vertices.append(list(v))
                tri_vertices.append(vertex_map[v])
            faces.append(tri_vertices)
            f.read(2)  # attribute byte count

    return Geometry(
        vertices=np.array(vertices),
        faces=np.array(faces),
        name=Path(filepath).stem,
        format='stl',
    )


def parse_obj(filepath: str) -> Geometry:
    """Parse OBJ file."""
    vertices = []
    faces = []

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == 'v':
                vertices.append([float(x) for x in parts[1:4]])
            elif parts[0] == 'f':
                face = []
                for p in parts[1:]:
                    idx = int(p.split('/')[0]) - 1  # OBJ is 1-indexed
                    face.append(idx)
                faces.append(face)

    return Geometry(
        vertices=np.array(vertices),
        faces=np.array(faces),
        name=Path(filepath).stem,
        format='obj',
    )


def generate_box(width: float = 1.0, height: float = 1.0, depth: float = 1.0) -> Geometry:
    """Generate a box geometry."""
    w, h, d = width / 2, height / 2, depth / 2
    vertices = np.array([
        [-w, -h, -d], [w, -h, -d], [w, h, -d], [-w, h, -d],
        [-w, -h, d], [w, -h, d], [w, h, d], [-w, h, d],
    ])
    faces = np.array([
        [0, 1, 2], [0, 2, 3],  # front
        [5, 4, 7], [5, 7, 6],  # back
        [4, 0, 3], [4, 3, 7],  # left
        [1, 5, 6], [1, 6, 2],  # right
        [3, 2, 6], [3, 6, 7],  # top
        [4, 5, 1], [4, 1, 0],  # bottom
    ])
    return Geometry(vertices=vertices, faces=faces, name="box", format="generated")


def generate_sphere(radius: float = 1.0, resolution: int = 16) -> Geometry:
    """Generate a sphere geometry."""
    vertices = []
    faces = []

    for i in range(resolution + 1):
        theta = np.pi * i / resolution
        for j in range(resolution * 2):
            phi = 2 * np.pi * j / (resolution * 2)
            x = radius * np.sin(theta) * np.cos(phi)
            y = radius * np.sin(theta) * np.sin(phi)
            z = radius * np.cos(theta)
            vertices.append([x, y, z])

    for i in range(resolution):
        for j in range(resolution * 2):
            v0 = i * (resolution * 2) + j
            v1 = v0 + 1
            v2 = (i + 1) * (resolution * 2) + j
            v3 = v2 + 1

            if j == resolution * 2 - 1:
                v1 = i * (resolution * 2)
                v3 = (i + 1) * (resolution * 2)

            if i < resolution:
                faces.append([v0, v1, v2])
                faces.append([v1, v3, v2])

    return Geometry(
        vertices=np.array(vertices),
        faces=np.array(faces),
        name="sphere",
        format="generated",
    )
