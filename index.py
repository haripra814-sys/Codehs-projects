class ThermalSystem:
    """Models the physical transfer of thermal energy across a localized vector."""
    def __init__(self, initial_temperatures: list):
        self.nodes = initial_temperatures
        self.k_factor = 0.25  # Thermal conductivity constant

    def simulate_conduction_step(self):
        """Applies the laws of thermodynamics to distribute energy evenly."""
        next_state = self.nodes.copy()
        # Calculate energy transfer between adjacent physical nodes
        for i in range(1, len(self.nodes) - 1):
            heat_flux = self.k_factor * (self.nodes[i-1] - 2*self.nodes[i] + self.nodes[i+1])
            next_state[i] += heat_flux
        self.nodes = next_state

    def display_energy_profile(self, step: int):
        profile = " | ".join(f"{temp:.1f}°C" for temp in self.nodes)
        return f"Step {step:02d} -> [ {profile} ]"

# --- Run the Physical Simulation ---
# A system with a high-heat center node radiating outwards
metal_rod = ThermalSystem(initial_temperatures=[20.0, 20.0, 100.0, 20.0, 20.0])

print("--- Initializing Thermodynamic Conduction Simulation ---")
for step in range(1, 6):
    metal_rod.simulate_conduction_step()
    print(metal_rod.display_energy_profile(step))