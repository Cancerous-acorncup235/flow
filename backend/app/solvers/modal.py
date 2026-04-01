"""
Modal Analysis Solver

Computes natural frequencies and mode shapes
using eigenvalue decomposition of the generalized
eigenvalue problem: K*phi = omega^2 * M * phi
"""

import numpy as np
from dataclasses import dataclass
from app.solvers.fea_v2 import Node2D, Element2D, MaterialV2, assemble_global_stiffness


def lumped_mass_matrix(
    nodes: list[Node2D],
    elements: list[Element2D],
    mat: MaterialV2,
) -> np.ndarray:
    """Assemble lumped mass matrix."""
    n_dof = 2 * len(nodes)
    M = np.zeros((n_dof, n_dof))

    for elem in elements:
        coords = np.array([[nodes[nid].x, nodes[nid].y] for nid in elem.node_ids])

        # Element area (for quad)
        x = coords[:, 0]
        y = coords[:, 1]
        area = 0.5 * abs(
            (x[1] - x[0]) * (y[2] - y[0]) - (x[2] - x[0]) * (y[1] - y[0]) +
            (x[2] - x[0]) * (y[3] - y[0]) - (x[3] - x[0]) * (y[2] - y[0])
        )

        # Lumped mass per node
        mass_per_node = mat.rho * mat.t * area / 4

        for nid in elem.node_ids:
            M[2*nid, 2*nid] += mass_per_node
            M[2*nid+1, 2*nid+1] += mass_per_node

    return M


@dataclass
class ModalResult:
    frequencies_hz: np.ndarray
    frequencies_rad: np.ndarray
    mode_shapes: np.ndarray
    n_modes: int

    def get_mode(self, mode_index: int) -> np.ndarray:
        """Get displacement pattern for a specific mode."""
        return self.mode_shapes[:, mode_index]


def solve_modal(
    nodes: list[Node2D],
    elements: list[Element2D],
    mat: MaterialV2,
    n_modes: int = 6,
    fixed_dofs: list[int] | None = None,
) -> ModalResult:
    """
    Solve eigenvalue problem for natural frequencies.

    Returns first n_modes natural frequencies and mode shapes.
    """
    # Assemble K and M
    K = assemble_global_stiffness(nodes, elements, mat)
    M = lumped_mass_matrix(nodes, elements, mat)

    n_dof = K.shape[0]

    # Apply fixed BCs by removing rows/cols
    if fixed_dofs:
        free_dofs = [i for i in range(n_dof) if i not in fixed_dofs]
    else:
        free_dofs = list(range(n_dof))

    K_ff = K[np.ix_(free_dofs, free_dofs)]
    M_ff = M[np.ix_(free_dofs, free_dofs)]

    # Solve generalized eigenvalue problem
    try:
        eigenvalues, eigenvectors = np.linalg.eigh(K_ff, M_ff + 1e-12 * np.eye(len(free_dofs)))
    except np.linalg.LinAlgError:
        # Fallback: standard eigenvalue
        Minv = np.linalg.inv(M_ff + 1e-12 * np.eye(len(free_dofs)))
        eigenvalues, eigenvectors = np.linalg.eigh(Minv @ K_ff)

    # Filter positive eigenvalues and sort
    positive = eigenvalues > 1e-6
    eigenvalues = eigenvalues[positive]
    eigenvectors = eigenvectors[:, positive]

    # Sort by frequency
    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Take first n_modes
    n_available = min(n_modes, len(eigenvalues))
    eigenvalues = eigenvalues[:n_available]
    eigenvectors = eigenvectors[:, :n_available]

    # Expand mode shapes to full DOF
    full_shapes = np.zeros((n_dof, n_available))
    for i, dof in enumerate(free_dofs):
        full_shapes[dof, :] = eigenvectors[i, :]

    frequencies_rad = np.sqrt(eigenvalues)
    frequencies_hz = frequencies_rad / (2 * np.pi)

    return ModalResult(
        frequencies_hz=frequencies_hz,
        frequencies_rad=frequencies_rad,
        mode_shapes=full_shapes,
        n_modes=n_available,
    )
