class MacroAllocationEngine:
    """Calculates systemic macronutrient distributions based on daily caloric targets
    and specific metabolic optimization vectors (Bodybuilding, Endurance, or Longevity).
    """
    def __init__(self, daily_calories: int):
        self.calories = daily_calories

    def allocate_macros(self, strategy: str) -> dict:
        """Splits total caloric volume into standard protein, carb, and fat gram requirements.
        1g Protein = 4 Calories | 1g Carb = 4 Calories | 1g Fat = 9 Calories
        """
        # Strategy Profiles (Representing percentage splits: [Protein, Carb, Fat])
        strategies = {
            "performance": [0.30, 0.50, 0.20],  # High carb for athletic output
            "composition": [0.40, 0.30, 0.30],  # High protein for muscle retention
            "metabolic": [0.25, 0.25, 0.50]     # High fat / low carb profile
        }

        if strategy not in strategies:
            raise ValueError(f"Unknown optimization strategy. Choose from: {list(strategies.keys())}")

        splits = strategies[strategy]
        
        # Calculate caloric allocations
        protein_cal = self.calories * splits[0]
        carb_cal = self.calories * splits[1]
        fat_cal = self.calories * splits[2]

        # Convert calories to raw mass (grams)
        protein_grams = protein_cal / 4
        carb_grams = carb_cal / 4
        fat_grams = fat_cal / 9

        return {
            "strategy_mode": strategy.upper(),
            "target_calories": self.calories,
            "allocation_grams": {
                "protein": round(protein_grams, 1),
                "carbohydrates": round(carb_grams, 1),
                "fats": round(fat_grams, 1)
            },
            "caloric_distribution": {
                "protein_kcal": round(protein_cal, 1),
                "carb_kcal": round(carb_cal, 1),
                "fat_kcal": round(fat_fat_kcal if 'fat_fat_kcal' in locals() else fat_cal, 1)
            }
        }


# =====================================================================
# RUNNING THE METABOLIC DATA AUDIT
# =====================================================================
if __name__ == "__main__":
    # Example: A baseline TDEE calculated from your Mifflin-St Jeor backend
    calculated_tdee = 2650 
    
    allocator = MacroAllocationEngine(daily_calories=calculated_tdee)
    
    # Audit a high-performance athletic split
    telemetry = allocator.allocate_macros(strategy="performance")
    
    print(f"--- Metabolic Profile: {telemetry['strategy_mode']} ---")
    print(f"Total Daily Energy Target: {telemetry['target_calories']} kcal")
    print("\nRequired Daily Mass Allocation:")
    for macro, grams in telemetry['allocation_grams'].items():
        print(f" -> {macro.capitalize()}: {grams}g")
        
    print("\nEnergy Density Distribution:")
    for source, kcal in telemetry['caloric_distribution'].items():
        print(f" -> {source.replace('_', ' ').upper()}: {kcal} kcal")