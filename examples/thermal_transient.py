"""
Example: Thermal Transient Analysis

Simulates cooling of a hot steel plate in ambient air.
"""

import sys
sys.path.insert(0, '../backend')

import numpy as np
from app.solvers.thermal_classic import ThermalMaterial


def main():
    print("Transient Thermal Analysis: Steel Plate Cooling")
    print("=" * 55)

    # Parameters
    nx, ny = 30, 30
    dx = dy = 0.01  # 1cm grid
    T_initial = 200.0  # °C
    T_ambient = 25.0   # °C
    h_conv = 10.0      # W/(m2*K) convection coefficient
    dt = 0.5           # time step (s)
    total_time = 600.0 # total simulation time (s)

    steel = ThermalMaterial(
        thermal_conductivity=50.0,
        density=7850,
        specific_heat=460,
    )

    # Thermal diffusivity
    alpha = steel.thermal_conductivity / (steel.density * steel.specific_heat)
    print(f"Material: Steel")
    print(f"Thermal diffusivity: {alpha*1e6:.2f} mm²/s")
    print(f"Initial temp: {T_initial}°C")
    print(f"Ambient temp: {T_ambient}°C")

    # Initialize temperature field
    T = np.ones((ny, nx)) * T_initial

    # Time stepping
    time = 0.0
    center_temps = []

    print(f"\n{'Time (s)':>10} | {'Center (°C)':>12} | {'Avg (°C)':>10}")
    print("-" * 40)

    while time < total_time:
        T_old = T.copy()

        # Interior nodes: Fourier's law
        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                d2Tdx2 = (T_old[i, j+1] - 2*T_old[i,j] + T_old[i, j-1]) / dx**2
                d2Tdy2 = (T_old[i+1, j] - 2*T_old[i,j] + T_old[i-1, j]) / dy**2
                T[i, j] = T_old[i, j] + alpha * dt * (d2Tdx2 + d2Tdy2)

        # Boundary: convection
        for i in range(ny):
            T[i, 0] = T[i, 0] - h_conv * dt / (steel.density * steel.specific_heat * dx) * (T[i, 0] - T_ambient)
            T[i, -1] = T[i, -1] - h_conv * dt / (steel.density * steel.specific_heat * dx) * (T[i, -1] - T_ambient)
        for j in range(nx):
            T[0, j] = T[0, j] - h_conv * dt / (steel.density * steel.specific_heat * dx) * (T[0, j] - T_ambient)
            T[-1, j] = T[-1, j] - h_conv * dt / (steel.density * steel.specific_heat * dx) * (T[-1, j] - T_ambient)

        time += dt
        center_temps.append((time, T[ny//2, nx//2]))

        if time % 60 < dt:
            print(f"{time:>10.0f} | {T[ny//2, nx//2]:>12.1f} | {np.mean(T):>10.1f}")

    print(f"\n✓ Simulation complete ({total_time:.0f}s simulated)")


if __name__ == "__main__":
    main()
