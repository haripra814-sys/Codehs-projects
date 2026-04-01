from __future__ import annotations
from dataclasses import dataclass


class Bone:
    """High-level model of a human long bone with key structural layers."""

    @dataclass
    class Periosteum:
        thickness_mm: float = 0.3
        vascularized: bool = True

        def describe(self) -> str:
            return (
                "Periosteum: thin, fibrous membrane covering the outer surface. "
                "Provides protection, pain sensation, and blood supply for bone repair."
            )

    @dataclass
    class CompactBone:
        osteon_count: int = 1000
        mineralization: float = 0.7  # relative index 0..1

        def describe(self) -> str:
            return (
                "CompactBone: dense cortical layer. "
                "Contains osteons (Haversian systems) that provide mechanical strength."
            )

        def bone_density(self) -> float:
            """
            Estimate bone density from osteon count and mineralization.
            Higher osteon count and mineralization -> greater density.
            """
            base_density = 0.8
            density = base_density + (self.osteon_count / 5000.0) + self.mineralization * 0.2
            return min(density, 1.5)  # physiological upper bound approximation

    @dataclass
    class MedullaryCavity:
        marrow_type: str = "red"
        volume_cc: float = 10.0

        def describe(self) -> str:
            return (
                "MedullaryCavity: inner cavity containing bone marrow. "
                "Red marrow produces blood cells; yellow stores fat."
            )

        def hematopoietic_capacity(self) -> str:
            return (
                "High" if self.marrow_type == "red" else "Moderate"
            )

    def __init__(
        self,
        name: str,
        periosteum: Bone.Periosteum,
        compact: Bone.CompactBone,
        medullary: Bone.MedullaryCavity,
    ) -> None:
        self.name = name
        self.periosteum = periosteum
        self.compact = compact
        self.medullary = medullary

    def display_anatomy(self) -> None:
        """Educational output explaining each major component."""
        print(f"Bone: {self.name}")
        print("Anatomy and function summary:")
        print(f" - {self.periosteum.describe()}")
        print(f" - {self.compact.describe()}")
        print(f" - {self.medullary.describe()}")
        print(
            f"Bone density (estimated): {self.compact.bone_density():.3f} g/cm³ "
            "(higher = stronger, lower = more fracture-prone)"
        )
        print(f"Marrow function: {self.medullary.hematopoietic_capacity()}")

    def check_fracture_risk(self, impact_force: float) -> str:
        """
        Determine if an impact causes fracture.
        Simple formula:
            critical_force = k * bone_density
        where k is a strength coefficient.
        """
        density = self.compact.bone_density()
        strength_coefficient = 500.0  # N per normalized density unit (arbitrary)
        critical_force = density * strength_coefficient

        if impact_force >= critical_force:
            return (
                f"Fracture likely (impact {impact_force:.1f} N >= critical {critical_force:.1f} N)."
            )
        return (
            f"Fracture unlikely (impact {impact_force:.1f} N < critical {critical_force:.1f} N)."
        )


if __name__ == "__main__":
    femur = Bone(
        name="Femur",
        periosteum=Bone.Periosteum(thickness_mm=0.4),
        compact=Bone.CompactBone(osteon_count=2500, mineralization=0.85),
        medullary=Bone.MedullaryCavity(marrow_type="yellow", volume_cc=12.5),
    )

    femur.display_anatomy()
    print(femur.check_fracture_risk(impact_force=1100.0))
    print(femur.check_fracture_risk(impact_force=1800.0))
