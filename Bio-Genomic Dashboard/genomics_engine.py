"""
PhyloShield Genomics Engine
===========================

This module implements the core bioinformatics computational engine for the PhyloShield
DNA Analysis Platform. The GenomicsEngine class provides quantitative methods for
comparative genomic analysis between human and animal DNA sequences, focusing on
sequence identity, guanine-cytosine content, and environmental health risk assessment.

Scientific Foundation:
- Sequence Identity: Measures the percentage of identical nucleotides between two aligned sequences
- GC Content: Proportion of guanine and cytosine bases, correlated with DNA thermal stability
- Health Risk Assessment: Models mutation rate prediction based on environmental gas levels (MQ-135 sensor)

Dependencies: Biopython (for sequence analysis), Pandas (for data handling)
"""

from Bio import pairwise2, SeqUtils
from Bio.Seq import Seq
import pandas as pd


class GenomicsEngine:
    """
    Core computational class for DNA sequence analysis and health risk modeling.

    This class encapsulates the mathematical and algorithmic approaches for:
    1. Pairwise sequence alignment and identity calculation
    2. GC content quantification
    3. Environmental health risk assessment via mutation rate prediction

    Methods are designed to be computationally efficient for web-based real-time analysis.
    """

    def __init__(self):
        """
        Initialize the GenomicsEngine with default parameters.

        Sets up alignment scoring matrices and environmental modeling constants.
        """
        # Smith-Waterman alignment parameters (match=2, mismatch=-1, gap_open=-0.5, gap_extend=-0.1)
        self.alignment_params = {
            'match': 2,
            'mismatch': -1,
            'gap_open': -0.5,
            'gap_extend': -0.1
        }

        # Environmental health modeling constants
        # Mutation rate baseline and gas sensitivity factor (empirical)
        self.mutation_baseline = 0.001  # 0.1% baseline mutation rate
        self.gas_sensitivity = 0.0005   # Mutation increase per ppm MQ-135

    def calculate_sequence_identity(self, seq1: str, seq2: str) -> float:
        """
        Calculate sequence identity between two DNA sequences using global alignment.

        This method employs the Needleman-Wunsch global alignment algorithm (implemented
        via Biopython's pairwise2) to align the sequences, then computes the percentage
        of identical positions.

        Parameters:
        -----------
        seq1 : str
            First DNA sequence (typically human)
        seq2 : str
            Second DNA sequence (typically animal)

        Returns:
        --------
        float
            Sequence identity percentage (0.0 to 100.0)

        Algorithm Notes:
        ---------------
        - Uses global alignment to ensure complete sequence comparison
        - Scoring: match=+2, mismatch=-1, gap_open=-0.5, gap_extend=-0.1
        - Identity = (matches / alignment_length) * 100
        """
        # Convert to Biopython Seq objects for validation
        seq1_obj = Seq(seq1.upper())
        seq2_obj = Seq(seq2.upper())

        # Perform global alignment
        alignments = pairwise2.align.globalms(
            seq1_obj, seq2_obj,
            self.alignment_params['match'],
            self.alignment_params['mismatch'],
            self.alignment_params['gap_open'],
            self.alignment_params['gap_extend']
        )

        if not alignments:
            return 0.0

        # Use the best alignment (highest score)
        best_alignment = alignments[0]

        # Calculate identity: count matches divided by alignment length
        seq1_aligned, seq2_aligned = best_alignment[0], best_alignment[1]
        matches = sum(1 for a, b in zip(seq1_aligned, seq2_aligned) if a == b and a != '-')
        alignment_length = len(seq1_aligned)

        identity = (matches / alignment_length) * 100 if alignment_length > 0 else 0.0

        return round(identity, 2)

    def calculate_gc_content(self, sequence: str) -> float:
        """
        Calculate guanine-cytosine (GC) content percentage in a DNA sequence.

        GC content is a fundamental genomic parameter that influences DNA stability,
        melting temperature, and evolutionary patterns. Higher GC content generally
        indicates greater thermal stability.

        Parameters:
        -----------
        sequence : str
            DNA sequence string

        Returns:
        --------
        float
            GC content percentage (0.0 to 100.0)

        Scientific Context:
        ------------------
        - GC content affects DNA duplex stability (ΔG ∝ GC%)
        - Correlated with codon usage bias and evolutionary rate
        - Clinical relevance: GC-rich regions may have different mutation patterns
        """
        seq_obj = Seq(sequence.upper())
        # Calculate GC content manually for compatibility
        gc_count = seq_obj.count('G') + seq_obj.count('C')
        total_length = len(seq_obj)
        gc_percent = (gc_count / total_length) * 100 if total_length > 0 else 0.0
        return round(gc_percent, 2)

    def calculate_health_risk(self, mq135_gas_level: float) -> dict:
        """
        Predict mutation rate based on environmental gas levels (MQ-135 sensor).

        This method models the relationship between air quality (measured via MQ-135
        gas sensor) and predicted DNA mutation rate. The model assumes that elevated
        gas levels (indicating poor air quality) correlate with increased oxidative
        stress and DNA damage.

        Parameters:
        -----------
        mq135_gas_level : float
            Gas concentration in ppm (parts per million) from MQ-135 sensor

        Returns:
        --------
        dict
            Dictionary containing:
            - 'predicted_mutation_rate': float (percentage)
            - 'risk_level': str ('Low', 'Moderate', 'High', 'Critical')
            - 'gas_level': float (input value)

        Model Assumptions:
        -----------------
        - Baseline mutation rate: 0.1% (natural background)
        - Linear relationship: mutation_rate = baseline + (gas_level * sensitivity)
        - Risk thresholds: <1% Low, 1-2% Moderate, 2-5% High, >5% Critical
        """
        # Calculate predicted mutation rate
        predicted_rate = self.mutation_baseline + (mq135_gas_level * self.gas_sensitivity)
        predicted_rate_percent = predicted_rate * 100

        # Determine risk level based on predicted rate
        if predicted_rate_percent < 1.0:
            risk_level = "Low"
        elif predicted_rate_percent < 2.0:
            risk_level = "Moderate"
        elif predicted_rate_percent < 5.0:
            risk_level = "High"
        else:
            risk_level = "Critical"

        return {
            'predicted_mutation_rate': round(predicted_rate_percent, 3),
            'risk_level': risk_level,
            'gas_level': mq135_gas_level
        }

    def analyze_sequences(self, human_seq: str, animal_seq: str, gas_level: float = 0.0) -> dict:
        """
        Comprehensive analysis pipeline for comparative genomic assessment.

        This method orchestrates the complete analysis workflow, integrating sequence
        comparison, GC content quantification, and health risk assessment into a
        unified report.

        Parameters:
        -----------
        human_seq : str
            Human DNA sequence
        animal_seq : str
            Animal DNA sequence
        gas_level : float, optional
            MQ-135 gas level in ppm (default: 0.0)

        Returns:
        --------
        dict
            Complete analysis report with all computed metrics
        """
        # Perform individual analyses
        sequence_identity = self.calculate_sequence_identity(human_seq, animal_seq)
        human_gc = self.calculate_gc_content(human_seq)
        animal_gc = self.calculate_gc_content(animal_seq)
        health_risk = self.calculate_health_risk(gas_level)

        # Compile comprehensive report
        report = {
            'sequence_identity': sequence_identity,
            'human_gc_content': human_gc,
            'animal_gc_content': animal_gc,
            'health_risk': health_risk,
            'comparison_summary': {
                'gc_difference': round(abs(human_gc - animal_gc), 2),
                'identity_category': self._categorize_identity(sequence_identity)
            }
        }

        return report

    def _categorize_identity(self, identity: float) -> str:
        """
        Categorize sequence identity into evolutionary relationship classes.

        Parameters:
        -----------
        identity : float
            Sequence identity percentage

        Returns:
        --------
        str
            Evolutionary relationship category
        """
        if identity >= 90:
            return "Very High (Closely Related Species)"
        elif identity >= 70:
            return "High (Same Genus)"
        elif identity >= 50:
            return "Moderate (Same Family)"
        elif identity >= 30:
            return "Low (Same Order)"
        else:
            return "Very Low (Distant Relationship)"