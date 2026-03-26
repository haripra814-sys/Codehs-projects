from __future__ import annotations
from typing import Dict


class Cell:
    """A generic biological cell representation.

    Attributes:
        nucleus (bool): True if the cell contains a nucleus.
        dna_sequence (str): The DNA sequence in uppercase letters (A/C/G/T).
    """

    def __init__(self, nucleus: bool, dna_sequence: str) -> None:
        self.nucleus = nucleus
        self.dna_sequence = dna_sequence.upper()

    def replicate(self) -> "Cell":
        """Return a replicated Cell instance with the same type and sequence."""
        return self.__class__(nucleus=self.nucleus, dna_sequence=self.dna_sequence)

    def gc_content(self) -> float:
        """Calculate GC-content percentage using dictionary counts."""
        counts: Dict[str, int] = {"A": 0, "C": 0, "G": 0, "T": 0}
        for base in self.dna_sequence:
            if base in counts:
                counts[base] += 1

        total = sum(counts.values())
        if total == 0:
            return 0.0

        gc = counts["G"] + counts["C"]
        return (gc / total) * 100.0


class PlantCell(Cell):
    """A plant cell with chloroplasts support."""

    def __init__(self, nucleus: bool, dna_sequence: str, chloroplast: bool) -> None:
        super().__init__(nucleus=nucleus, dna_sequence=dna_sequence)
        self.chloroplast = chloroplast

    def photosynthesize(self) -> str:
        """Return a simple message representing the photosynthesis capability."""
        if self.chloroplast:
            return "Converting light to glucose"
        return "No chloroplast available"


class AnimalCell(Cell):
    """An animal cell with centriole support."""

    def __init__(self, nucleus: bool, dna_sequence: str, centriole: bool) -> None:
        super().__init__(nucleus=nucleus, dna_sequence=dna_sequence)
        self.centriole = centriole
