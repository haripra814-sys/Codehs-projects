"""Space DNA Integrity Simulator.

Stochastic model for oxidative DNA lesions in spaceflight conditions.
"""

import argparse
import random
from dataclasses import dataclass
from typing import Dict, List

import matplotlib.pyplot as plt

from strings_es import SPANISH_STRINGS

# Real human telomere repeat unit used as default test case.
# Guanine has the lowest oxidation potential among DNA bases, so
# oxidative stress is most likely to damage 'G' and form 8-oxoG.
DEFAULT_TELOMERE_SEQUENCE = "TTAGGG" * 20
DEFAULT_DAYS = 365
GROUND_CONTROL_RISK = 0.0001
SPACE_RISK = 0.012
RANDOM_SEED = 42

ENGLISH_STRINGS: Dict[str, str] = {
    "title": "=== Space DNA Integrity Simulator ===",
    "mission_days": "Mission duration (days): {days}",
    "sequence_length": "DNA length (bases): {length}",
    "sequence_preview": "DNA preview: {preview}...",
    "space_result": (
        "Space mission result -> 8-oxoG lesions: {lesions} | "
        "Integrity Score: {score:.2f}%"
    ),
    "ground_result": (
        "Ground control result -> 8-oxoG lesions: {lesions} | "
        "Integrity Score: {score:.2f}%"
    ),
    "chart_saved": "Chart saved to: {path}",
    "language_note": "Language mode: English",
}


@dataclass
class SimulationResult:
    label: str
    total_lesions: int
    final_integrity_score: float
    daily_scores: List[float]


def get_strings(language: str) -> Dict[str, str]:
    """Return localized output strings."""
    if language.lower() == "es":
        return SPANISH_STRINGS
    return ENGLISH_STRINGS


def mutate_one_day(dna_sites: List[str], daily_risk: float, rng: random.Random) -> int:
    """Mutate Guanine to 8-oxoG based on daily radiation risk."""
    lesions_today = 0
    for idx, base in enumerate(dna_sites):
        if base == "G" and rng.random() < daily_risk:
            dna_sites[idx] = "8-oxoG"
            lesions_today += 1
    return lesions_today


def integrity_score(dna_sites: List[str]) -> float:
    """Compute percentage of bases that remain unmutated."""
    damaged = dna_sites.count("8-oxoG")
    return ((len(dna_sites) - damaged) / len(dna_sites)) * 100.0


def run_mission(
    label: str,
    dna_sequence: str,
    days: int,
    daily_risk: float,
    rng: random.Random,
) -> SimulationResult:
    """Run a full mission and return time-series integrity metrics."""
    dna_sites = list(dna_sequence.upper())
    daily_scores: List[float] = []
    total_lesions = 0

    for _day in range(1, days + 1):
        total_lesions += mutate_one_day(dna_sites, daily_risk, rng)
        daily_scores.append(integrity_score(dna_sites))

    return SimulationResult(
        label=label,
        total_lesions=total_lesions,
        final_integrity_score=daily_scores[-1] if daily_scores else 100.0,
        daily_scores=daily_scores,
    )


def plot_integrity(space: SimulationResult, ground: SimulationResult, output_path: str) -> None:
    """Generate a bar chart for final DNA integrity after mission."""
    labels = [space.label, ground.label]
    scores = [space.final_integrity_score, ground.final_integrity_score]
    colors = ["#d9534f", "#5cb85c"]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, scores, color=colors)
    plt.ylim(0, 100)
    plt.ylabel("Integrity Score (%)")
    plt.title("DNA Integrity After 365-Day Mission")

    for bar, score in zip(bars, scores):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{score:.2f}%",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simulate space radiation damage to DNA.")
    parser.add_argument(
        "--language",
        choices=["en", "es"],
        default="en",
        help="Console output language (en or es).",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_DAYS,
        help="Number of days to simulate (default: 365).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    strings = get_strings(args.language)
    rng = random.Random(RANDOM_SEED)

    space = run_mission(
        label="Space",
        dna_sequence=DEFAULT_TELOMERE_SEQUENCE,
        days=args.days,
        daily_risk=SPACE_RISK,
        rng=rng,
    )
    ground = run_mission(
        label="Ground Control",
        dna_sequence=DEFAULT_TELOMERE_SEQUENCE,
        days=args.days,
        daily_risk=GROUND_CONTROL_RISK,
        rng=rng,
    )

    chart_path = "integrity_score_365_days.png"
    plot_integrity(space, ground, chart_path)

    print(strings["title"])
    print(strings["language_note"])
    print(strings["mission_days"].format(days=args.days))
    print(strings["sequence_length"].format(length=len(DEFAULT_TELOMERE_SEQUENCE)))
    print(strings["sequence_preview"].format(preview=DEFAULT_TELOMERE_SEQUENCE[:24]))
    print(
        strings["space_result"].format(
            lesions=space.total_lesions,
            score=space.final_integrity_score,
        )
    )
    print(
        strings["ground_result"].format(
            lesions=ground.total_lesions,
            score=ground.final_integrity_score,
        )
    )
    print(strings["chart_saved"].format(path=chart_path))


if __name__ == "__main__":
    main()