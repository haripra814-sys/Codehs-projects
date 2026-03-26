import random

class Plant:
    """
    A class to simulate the biological processes of a plant.
    This demonstrates the relationship between light, water, and growth.
    """
    def __init__(self, species: str):
        self.species = species
        self.height = 1.0  # in centimeters
        self.energy_reserves = 5.0
        self.is_alive = True
        self.has_chloroplasts = True # Unique to plants!

    def photosynthesis(self, light_intensity: int, water_level: int) -> str:
        """
        Explains the chemical reaction: 6CO2 + 6H2O + light -> C6H12O6 + 6O2
        """
        if water_level > 2 and light_intensity > 5:
            generation = (light_intensity * 0.5) + (water_level * 0.2)
            self.energy_reserves += generation
            return f"🌿 Photosynthesis successful! Generated {generation:.2f} glucose."
        else:
            self.energy_reserves -= 1.0
            return "⚠️ Not enough light or water. Consuming stored energy..."

    def grow(self):
        """Uses energy reserves to increase plant biomass."""
        if self.energy_reserves > 10:
            growth_amount = random.uniform(0.5, 2.0)
            self.height += growth_amount
            self.energy_reserves -= 5 # Growth costs energy!
            print(f"🌱 Growth spurt! {self.species} is now {self.height:.2f}cm tall.")
        
        if self.energy_reserves <= 0:
            self.is_alive = False
            print("🥀 The plant has wilted due to lack of energy.")

# --- Running the Simulation ---
my_sunflower = Plant("Sunflower")

print(f"--- Starting Biology Simulation: {my_sunflower.species} ---")

# Simulate 5 days of life
for day in range(1, 6):
    print(f"\nDay {day}:")
    # Simulate random environment
    sun = random.randint(1, 10)
    water = random.randint(1, 5)
    
    print(my_sunflower.photosynthesis(sun, water))
    my_sunflower.grow()
    
    if not my_sunflower.is_alive:
        break