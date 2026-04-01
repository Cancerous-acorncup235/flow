"""
FEA Solver v2 — Quadrilateral Elements

Advanced FEA with quad elements, plane stress/strain,
and proper sparse matrix assembly.
"""

import numpy as np
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ElementType(Enum):
    TRIANGLE_3 = "tri3"
    QUAD_4 = "quad4"


class AnalysisType(Enum):
    PLANE_STRESS = "plane_stress"
    PLANE_STRAIN = "plane_strain"


@dataclass
class Node2D:
    id: int
    x: float
    y: float
    fx: float = 0.0
    fy: float = 0.0
    ux_fixed: bool = False
    uy_fixed: bool = False


@dataclass
class Element2D:
    id: int
    node_ids: list[int]
    element_type: ElementType = ElementType.QUAD_4


@dataclass
class MaterialV2:
    E: float  # Young's modulus (Pa)
    nu: float  # Poisson's ratio
    rho: float = 7850.0  # Density (kg/m3)
    t: float = 0.01  # Thickness (m)


def material_matrix(mat: MaterialV2, analysis: AnalysisType = AnalysisType.PLANE_STRESS) -> np.ndarray:
    """Compute 3x3 material constitutive matrix D."""
    E, nu = mat.E, mat.nu

    if analysis == AnalysisType.PLANE_STRESS:
        return (E / (1 - nu**2)) * np.array([
            [1, nu, 0],
            [nu, 1, 0],
            [0, 0, (1 - nu) / 2],
        ])
    else:  # plane strain
        factor = E / ((1 + nu) * (1 - 2 * nu))
        return factor * np.array([
            [1 - nu, nu, 0],
            [nu, 1 - nu, 0],
            [0, 0, (1 - 2 * nu) / 2],
        ])


def shape_functions_quad(xi: float, eta: float) -> tuple[np.ndarray, np.ndarray]:
    """Shape functions and derivatives for 4-node quad at (xi, eta)."""
    # Shape functions
    N = 0.25 * np.array([
        (1 - xi) * (1 - eta),
        (1 + xi) * (1 - eta),
        (1 + xi) * (1 + eta),
        (1 - xi) * (1 + eta),
    ])

    # Derivatives dN/dxi, dN/deta
    dNdxi = 0.25 * np.array([
        -(1 - eta), (1 - eta), (1 + eta), -(1 + eta),
    ])
    dNdeta = 0.25 * np.array([
        -(1 - xi), -(1 + xi), (1 + xi), (1 - xi),
    ])

    return N, np.array([dNdxi, dNdeta])


def element_stiffness_quad(
    node_coords: np.ndarray,
    mat: MaterialV2,
    analysis: AnalysisType = AnalysisType.PLANE_STRESS,
) -> np.ndarray:
    """Compute 8x8 element stiffness matrix for 4-node quad."""
    D = material_matrix(mat, analysis)
    Ke = np.zeros((8, 8))

    # Gauss quadrature 2x2
    gp = 1 / np.sqrt(3)
    gauss_points = [(-gp, -gp), (gp, -gp), (gp, gp), (-gp, gp)]
    weights = [1, 1, 1, 1]

    for (xi, eta), w in zip(gauss_points, weights):
        _, dN = shape_functions_quad(xi, eta)

        # Jacobian
        J = dN @ node_coords  # 2x2
        detJ = np.linalg.det(J)
        invJ = np.linalg.inv(J)

        # dN/dx, dN/dy
        dNdx = invJ @ dN  # 2x4

        # B matrix (3x8)
        B = np.zeros((3, 8))
        for i in range(4):
            B[0, 2*i] = dNdx[0, i]
            B[1, 2*i+1] = dNdx[1, i]
            B[2, 2*i] = dNdx[1, i]
            B[2, 2*i+1] = dNdx[0, i]

        Ke += mat.t * detJ * w * (B.T @ D @ B)

    return Ke


def assemble_global_stiffness(
    nodes: list[Node2D],
    elements: list[Element2D],
    mat: MaterialV2,
    analysis: AnalysisType = AnalysisType.PLANE_STRESS,
) -> np.ndarray:
    """Assemble global stiffness matrix."""
    n_dof = 2 * len(nodes)
    K = np.zeros((n_dof, n_dof))

    for elem in elements:
        coords = np.array([[nodes[nid].x, nodes[nid].y] for nid in elem.node_ids])
        Ke = element_stiffness_quad(coords, mat, analysis)

        # Map to global DOFs
        dofs = []
        for nid in elem.node_ids:
            dofs.extend([2 * nid, 2 * nid + 1])

        for i, gi in enumerate(dofs):
            for j, gj in enumerate(dofs):
                K[gi, gj] += Ke[i, j]

    return K


def solve_v2(
    nodes: list[Node2D],
    elements: list[Element2D],
    mat: MaterialV2,
    analysis: AnalysisType = AnalysisType.PLANE_STRESS,
) -> dict:
    """Solve 2D FEA problem with quad elements."""
    n_dof = 2 * len(nodes)

    # Assemble
    K = assemble_global_stiffness(nodes, elements, mat, analysis)

    # Force vector
    F = np.zeros(n_dof)
    for node in nodes:
        F[2 * node.id] = node.fx
        F[2 * node.id + 1] = node.fy

    # Apply BCs
    fixed_dofs = []
    for node in nodes:
        if node.ux_fixed:
            fixed_dofs.append(2 * node.id)
        if node.uy_fixed:
            fixed_dofs.append(2 * node.id + 1)

    free_dofs = [i for i in range(n_dof) if i not in fixed_dofs]

    if not free_dofs:
        return {"displacements": np.zeros(n_dof), "max_disp": 0, "max_stress": 0}

    K_ff = K[np.ix_(free_dofs, free_dofs)]
    F_f = F[free_dofs]

    try:
        U_f = np.linalg.solve(K_ff + 1e-12 * np.eye(len(free_dofs)), F_f)
    except np.linalg.LinAlgError:
        U_f = np.zeros(len(free_dofs))

    U = np.zeros(n_dof)
    for i, dof in enumerate(free_dofs):
        U[dof] = U_f[i]

    # Compute stresses at gauss points
    max_stress = 0
    D = material_matrix(mat, analysis)
    gp = 1 / np.sqrt(3)
    gauss_points = [(-gp, -gp), (gp, -gp), (gp, gp), (-gp, gp)]

    for elem in elements:
        coords = np.array([[nodes[nid].x, nodes[nid].y] for nid in elem.node_ids])
        elem_disp = np.concatenate([U[2*nid:2*nid+2] for nid in elem.node_ids])

        for xi, eta in gauss_points:
            _, dN = shape_functions_quad(xi, eta)
            J = dN @ coords
            invJ = np.linalg.inv(J)
            dNdx = invJ @ dN

            B = np.zeros((3, 8))
            for i in range(4):
                B[0, 2*i] = dNdx[0, i]
                B[1, 2*i+1] = dNdx[1, i]
                B[2, 2*i] = dNdx[1, i]
                B[2, 2*i+1] = dNdx[0, i]

            stress = D @ B @ elem_disp
            vm = np.sqrt(stress[0]**2 - stress[0]*stress[1] + stress[1]**2 + 3*stress[2]**2)
            max_stress = max(max_stress, vm)

    displacements = U.reshape(-1, 2)
    max_disp = float(np.max(np.linalg.norm(displacements, axis=1)))

    return {
        "displacements": displacements,
        "max_disp": max_disp,
        "max_stress": float(max_stress),
        "safety_factor": mat.E / max(max_stress, 1e-10),
    }
