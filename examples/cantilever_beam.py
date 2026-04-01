"""
Example: Cantilever Beam with Distributed Load

Analyzes a cantilever beam fixed at one end with uniform load.
Compares FEA results with analytical solution.
"""

import sys
sys.path.insert(0, '../backend')

import numpy as np
from app.solvers.fea_classic import generate_beam_mesh, solve, Material


def analytical_cantilever(L, h, b, E, q):
    """Analytical solution for cantilever beam with uniform load."""
    I = b * h**3 / 12  # Moment of inertia
    max_deflection = q * L**4 / (8 * E * I)
    max_stress = q * L**2 / (2 * (b * h**2 / 6))
    return max_deflection, max_stress


def main():
    print("Cantilever Beam Analysis: FEA vs Analytical")
    print("=" * 55)

    # Beam parameters
    L = 2.0       # Length (m)
    h = 0.1       # Height (m)
    b = 0.05      # Width (m)
    q = 5000      # Distributed load (N/m)

    # Material
    steel = Material(
        youngs_modulus=200e9,
        poissons_ratio=0.3,
        density=7850,
        thickness=b,
    )

    # Mesh convergence study
    mesh_sizes = [5, 10, 20, 40]
    print(f"\nBeam: {L}m x {h}m x {b}m")
    print(f"Load: {q} N/m (uniform)")
    print(f"Material: Steel (E={steel.youngs_modulus/1e9:.0f} GPa)")

    # Analytical solution
    defl_analytical, stress_analytical = analytical_cantilever(L, h, b, steel.youngs_modulus, q)
    print(f"\nAnalytical Solution:")
    print(f"  Max deflection: {defl_analytical*1000:.4f} mm")
    print(f"  Max stress: {stress_analytical/1e6:.2f} MPa")

    # FEA convergence
    print(f"\n{'Mesh':>6} | {'Deflection (mm)':>15} | {'Error %':>8}")
    print("-" * 40)

    for n in mesh_sizes:
        mesh = generate_beam_mesh(length=L, height=h, nx=n*2, ny=n//2, material=steel)
        result = solve(mesh)

        error = abs(result.max_displacement - defl_analytical) / defl_analytical * 100
        print(f"  {n:>4} | {result.max_displacement*1000:>15.4f} | {error:>7.1f}%")

    print("\n✓ Convergence study complete")


if __name__ == "__main__":
    main()
