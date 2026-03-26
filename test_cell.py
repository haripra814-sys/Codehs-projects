import unittest

from cell import AnimalCell, Cell, PlantCell


class TestCellBiologyLogic(unittest.TestCase):
    # In a bioinformatics lab, regression tests prevent subtle data corruption
    # and ensure scientific transformations remain valid across code updates.

    def test_replicate_produces_same_type(self):
        plant = PlantCell(nucleus=True, dna_sequence="ATGC", chloroplast=True)
        baby = plant.replicate()

        self.assertIsInstance(baby, PlantCell)
        self.assertEqual(baby.dna_sequence, plant.dna_sequence)
        self.assertEqual(baby.nucleus, plant.nucleus)

    def test_gc_content_of_known_sequence(self):
        cell = Cell(nucleus=True, dna_sequence="GGCG")
        self.assertEqual(cell.gc_content(), 100.0)

    def test_inheritance(self):
        plant = PlantCell(nucleus=True, dna_sequence="ATGC", chloroplast=True)
        self.assertIsInstance(plant, Cell)

    def test_empty_sequence_gc_content(self):
        empty = Cell(nucleus=True, dna_sequence="")
        self.assertEqual(empty.gc_content(), 0.0)


if __name__ == "__main__":
    unittest.main()
