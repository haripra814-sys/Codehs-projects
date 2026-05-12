import abc
import time

# --- The Strategy Interface (The Abstract Plan) ---
class ActionStrategy(abc.ABC):
    """Defines a family of logical responses."""
    @abc.abstractmethod
    def execute(self, data: dict) -> str:
        pass

# --- Concrete Strategies (The Master's Options) ---
class MinimumEffort(ActionStrategy):
    """Ayanokoji's default state: Win with the least movement possible."""
    def execute(self, data: dict) -> str:
        return f"[LOGIC] Threshold met. Deploying minimum necessary intervention for {data['target']}."

class SystemicOverhaul(ActionStrategy):
    """Used only when the 'game' requires a total change of the board."""
    def execute(self, data: dict) -> str:
        return f"[LOGIC] Tactical necessity detected. Rewriting system parameters for {data['target']}."

class DefensiveShadow(ActionStrategy):
    """Obscure the true intent while maintaining control."""
    def execute(self, data: dict) -> str:
        return f"[LOGIC] Redirecting attention. Controlling outcome from the periphery."

# --- The Context (The 'White Room' Logic Controller) ---
class Strategist:
    def __init__(self, initial_strategy: ActionStrategy):
        self._strategy = initial_strategy

    def set_strategy(self, new_strategy: ActionStrategy):
        print(f"[SYSTEM] Switching to {new_strategy.__class__.__name__}...")
        self._strategy = new_strategy

    def process_scenario(self, scenario: dict):
        # Ayanokoji-style analysis: Calculating the path of least resistance
        print(f"--- Analyzing Scenario: {scenario['id']} ---")
        time.sleep(0.5)  # Processing time
        result = self._strategy.execute(scenario)
        print(result)

# --- Execution ---
if __name__ == "__main__":
    # Initialize with Minimum Effort (Standard Ayanokoji)
    kiyotaka = Strategist(MinimumEffort())
    
    current_scenario = {"id": "Class D Conflict", "target": "Horikita"}
    kiyotaka.process_scenario(current_scenario)
    
    # Change strategy based on shifting variables
    print("\n[ALERT] Variable Change: Interference from Class A detected.")
    kiyotaka.set_strategy(DefensiveShadow())
    kiyotaka.process_scenario(current_scenario)