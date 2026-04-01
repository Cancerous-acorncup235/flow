"""
Example: Beam Deflection Analysis

Run a simple FEA simulation on a steel beam.
"""

import sys
sys.path.insert(0, '../backend')

from app.solvers.fea_classic import generate_beam_mesh, solve, Material


def main():
    print("FLOW Example: Beam Deflection Analysis")
    print("=" * 50)

    # Define material (steel)
    steel = Material(
        youngs_modulus=200e9,  # 200 GPa
        poissons_ratio=0.3,
        density=7850,  # kg/m3
        thickness=0.01,  # 10mm
    )

    # Generate mesh
    print("\nGenerating beam mesh...")
    mesh = generate_beam_mesh(
        length=2.0,    # 2 meters
        height=0.15,   # 150mm
        nx=20,         # 20 elements along length
        ny=4,          # 4 elements across height
        material=steel,
    )
    print(f"  Nodes: {len(mesh.nodes)}")
    print(f"  Elements: {len(mesh.elements)}")
    print(f"  Material: Steel (E={steel.youngs_modulus/1e9:.0f} GPa)")

    # Solve
    print("\nRunning FEA solver...")
    result = solve(mesh)

    # Results
    print(f"\nResults:")
    print(f"  Max displacement: {result.max_displacement*1000:.3f} mm")
    print(f"  Max von Mises stress: {result.max_stress/1e6:.2f} MPa")
    print(f"  Safety factor: {result.safety_factor:.2f}")

    if result.safety_factor > 2.0:
        print("\n  ✓ Structure is SAFE (SF > 2.0)")
    else:
        print("\n  ⚠ Structure may need reinforcement")

    print("\n" + "=" * 50)
    print("Simulation complete.")


if __name__ == "__main__":
    main()
