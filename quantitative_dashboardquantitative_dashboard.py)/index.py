import reflex as rx

class DashboardState(rx.State):
    """The Backend Logic Gate: State Management Engine."""
    target_objective: str = "Hypertrophy"
    weight_kg: float = 70.0
    height_cm: float = 175.0
    calculated_bmr: float = 0.0
    is_calculated: bool = False

    def calculate_metabolic_baseline(self):
        """Pure mathematical execution for basal metabolic rate (Mifflin-St Jeor)."""
        # Logic: Deterministic calculation based on physical variables
        self.calculated_bmr = (10.0 * self.weight_kg) + (6.25 * self.height_cm) - (5.0 * 18.0) + 5.0
        self.is_calculated = True

def index() -> rx.Component:
    """The Frontend Interface Engine: Constructed 100% out of Python objects."""
    return rx.center(
        rx.vstack(
            rx.heading("Systemic Biometric Dashboard", size="7", color="#F3F4F6"),
            rx.text(
                "Algorithmic optimization platform for metabolic allocation models.",
                color="#9CA3AF"
            ),
            rx.divider(border_color="#374151"),
            
            # Input Control Matrix
            rx.vstack(
                rx.text("Current Metric Mass (KG):", color="#E5E7EB"),
                rx.input(
                    value=DashboardState.weight_kg.to_string(),
                    on_change=DashboardState.set_weight_kg,
                    background_color="#1F2937",
                    border_color="#4B5563",
                    color="#F3F4F6"
                ),
                rx.text("Current Kinetic Height (CM):", color="#E5E7EB"),
                rx.input(
                    value=DashboardState.height_cm.to_string(),
                    on_change=DashboardState.set_height_cm,
                    background_color="#1F2937",
                    border_color="#4B5563",
                    color="#F3F4F6"
                ),
                align_items="start",
                width="100%"
            ),
            
            # Execution Trigger
            rx.button(
                "Run Metabolic Audit",
                on_click=DashboardState.calculate_metabolic_baseline,
                background_color="#2563EB",
                color="#FFFFFF",
                _hover={"background_color": "#1D4ED8"},
                width="100%"
            ),
            
            # Conditional Telemetry Output
            rx.cond(
                DashboardState.is_calculated,
                rx.box(
                    rx.text(f"Calculated Basal Capacity: {DashboardState.calculated_bmr} kcal/day", color="#10B981", weight="bold"),
                    background_color="#111827",
                    padding="4",
                    border_radius="md",
                    border="1px solid #059669",
                    width="100%"
                )
            ),
            
            spacing="5",
            padding="8",
            background_color="#111827",
            border_radius="lg",
            border="1px solid #374151",
            max_width="450px",
            width="100%"
        ),
        width="100%",
        height="100vh",
        background_color="#030712"
    )

# --- App Compilation Configuration ---
app = rx.App()
app.add_page(index)