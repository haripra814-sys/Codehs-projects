# Space-DNA-Integrity-Sim

Computational biology simulation for modeling oxidative DNA damage during long-duration spaceflight.

## Project Idea

This project treats DNA like a biological data system. In computer memory, radiation can cause a **bit flip** (for example, `0` becomes `1`). In biology, oxidative stress can cause a molecular "flip" where Guanine (`G`) is oxidized into **8-oxoguanine (`8-oxoG`)**, which can lead to replication errors.

The simulator uses a stochastic (random) model to estimate how much DNA integrity is preserved over a 365-day mission.

## Why Guanine?

Guanine has the lowest oxidation potential among the four DNA bases, so it is the most chemically vulnerable to oxidation damage under radiation stress.

## Real DNA Test Case

The default sequence is based on the real human telomere repeat:

`TTAGGG`

Telomeres are biologically important and naturally rich in Guanine, making them a useful model for oxidative damage studies.

## Space vs Ground Control

The simulation compares:

- **Space mission:** elevated daily radiation risk
- **Ground Control (Earth):** near-zero daily risk

This provides a clean baseline comparison for how cosmic radiation changes DNA integrity.

## Visual Output

The script creates a bar chart:

- `integrity_score_365_days.png`

The chart compares final DNA integrity scores for Space and Ground Control after 365 days.

## Genes in Space Relevance

The [Genes in Space](https://www.genesinspace.org/) competition encourages student-designed experiments in molecular biology and space research. This project aligns with that mission by:

- integrating molecular biology concepts (oxidative DNA damage)
- using computational modeling to test hypotheses
- generating interpretable outputs for science communication

## Setup

```bash
pip install -r requirements.txt
```

## Run

English output:

```bash
python simulator.py
```

Spanish output:

```bash
python simulator.py --language es
```

Optional custom mission length:

```bash
python simulator.py --days 365
```

## Files

- `simulator.py` - core stochastic model, Space vs Ground comparison, chart generation
- `strings_es.py` - Spanish localization for console output
- `requirements.txt` - Python dependencies