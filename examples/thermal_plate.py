"""
Example: Heat Conduction in a Steel Plate

Run a 2D thermal simulation on a rectangular plate.
"""

import sys
sys.path.insert(0, '../backend')

from app.solvers.thermal_classic import generate_plate_mesh, solve, ThermalMaterial


def main():
    print("FLOW Example: 2D Heat Conduction")
    print("=" * 50)

    # Define material (steel)
    steel = ThermalMaterial(
        thermal_conductivity=50.0,  # W/(m*K)
        density=7850,
        specific_heat=460,
    )

    # Generate mesh
    print("\nGenerating plate mesh...")
    mesh = generate_plate_mesh(
        width=0.5,   # 50cm
        height=0.5,  # 50cm
        nx=50,
        ny=50,
        material=steel,
    )
    print(f"  Grid: {mesh.nx}x{mesh.ny}")
    print(f"  Material: Steel (k={steel.thermal_conductivity} W/mK)")

    # Solve
    print("\nRunning thermal solver...")
    result = solve(
        mesh,
        T_left=100.0,   # Hot left wall
        T_right=20.0,   # Cold right wall
        T_top=50.0,     # Warm top
        T_bottom=50.0,  # Warm bottom
    )

    # Results
    print(f"\nResults:")
    print(f"  Max temperature: {result.max_temp:.1f} °C")
    print(f"  Min temperature: {result.min_temp:.1f} °C")
    print(f"  Max heat flux: {result.max_flux:.1f} W/m²")
    print(f"  Center temperature: {result.temperature[25, 25]:.1f} °C")

    print("\n" + "=" * 50)
    print("Simulation complete.")


if __name__ == "__main__":
    main()
