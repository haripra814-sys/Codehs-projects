# Bioinformatics Cell Model

This repository demonstrates a small Python object-oriented model for a biological cell system.

## Files

- `cell.py`: Implements `Cell`, `PlantCell`, `AnimalCell` classes, with replication and GC content calculation.
- `test_cell.py`: `unittest` suite validating behavior and edge cases.

## How it works

- `Cell` is a base class with attributes `nucleus` and `dna_sequence`.
- `dna_sequence` is normalized to uppercase on initialization.
- `Cell.replicate()` creates a new instance via `self.__class__` so subclass behavior is preserved.
- `Cell.gc_content()` counts bases in a dictionary and returns `(G+C)/total * 100`.

### Subclasses

- `PlantCell` adds `chloroplast` and a `photosynthesize()` method.
- `AnimalCell` adds `centriole` only.

## Why this design

- This is a portfolio-friendly OOP design with inheritance and clear single responsibility.
- `replicate()` returns the same type using `self.__class__` rather than hardcoding `Cell`.
- `gc_content()` uses explicit nucleotide dictionary for biological correctness and to ignore invalid chars.

## Bugs encountered and why it's written this way

1. Initial implementation used `return Cell(...)` in `replicate()`.
   - Bug: replicating a `PlantCell` produced a `Cell`, losing subclass-specific data structure.
   - Fix: use `self.__class__` so every class replicates as its own type.

2. `gc_content()` first version did not handle empty strings.
   - Bug: division by zero crash when DNA is empty.
   - Fix: check `total == 0` and return `0.0`.

3. Lowercase DNA input was unhandled in earlier versions.
   - Bug: counts could be wrong or skip lower-case letters.
   - Fix: uppercase conversion in the constructor.

## Running tests

```bash
python -m unittest test_cell.py
```

## Notes

- This project emphasizes test-driven confidence in computational biology logic.
- Treat unit tests as scientific validation for code correctness across experiments.
