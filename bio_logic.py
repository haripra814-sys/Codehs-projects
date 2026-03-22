"""
BioCross-Alpha Computational Biology Engine
==========================================

This module encapsulates the core bioinformatics algorithms for analyzing
genomic and proteomic sequences in the context of cross-species health assessment.
Utilizing Biopython's robust library, we implement sequence alignment, compositional
analysis, and zoonotic risk evaluation to elucidate potential interspecies
transmission mechanisms and biological compatibilities.

Author: Senior Bioinformatics Engineer
Date: March 21, 2026
"""

from Bio.Align import PairwiseAligner
from Bio.SeqUtils import molecular_weight
from Bio.SeqUtils.IsoelectricPoint import IsoelectricPoint
from Bio.Seq import Seq


class BioAnalyzer:
    """
    BioAnalyzer Class: A comprehensive engine for computational biology analysis.

    This class serves as the nucleus of our bioinformatics pipeline, integrating
    sequence alignment techniques, compositional metrics, and risk assessment
    algorithms to dissect nucleotide and amino acid sequences for insights into
    evolutionary conservation and zoonotic potential.
    """

    def __init__(self):
        """
        Initialize the BioAnalyzer with default parameters for sequence processing.
        """
        pass

    def align_sequences(self, seq1, seq2):
        """
        Perform pairwise global sequence alignment between two biological sequences.

        This method employs the Needleman-Wunsch algorithm via Biopython's PairwiseAligner
        module to compute optimal global alignments, revealing nucleotide polymorphisms,
        insertions, deletions, and conserved regions that may indicate functional
        homology between human and animal orthologs.

        Parameters:
        - seq1 (str): The first sequence (e.g., human gene sequence).
        - seq2 (str): The second sequence (e.g., animal ortholog).

        Returns:
        - dict: Alignment results including score, aligned sequences, and metadata.
        """
        # Convert to uppercase for consistency
        seq1 = seq1.upper()
        seq2 = seq2.upper()

        # Initialize aligner with global alignment parameters
        aligner = PairwiseAligner()
        aligner.mode = 'global'
        aligner.match_score = 2
        aligner.mismatch_score = -1
        aligner.open_gap_score = -0.5
        aligner.extend_gap_score = -0.1

        # Perform alignment
        alignments = aligner.align(seq1, seq2)

        if alignments:
            best_alignment = alignments[0]
            return {
                'score': best_alignment.score,
                'seq1_aligned': str(best_alignment[0]),
                'seq2_aligned': str(best_alignment[1]),
                'start_end_positions': None  # Not applicable in new API
            }
        else:
            return {'error': 'No alignment possible'}

    def analyze_composition(self, sequence):
        """
        Analyze the biochemical composition of a given nucleotide or amino acid sequence.

        This function computes key physicochemical properties including GC-content
        (indicative of thermal stability in DNA), molecular weight (total mass of
        nucleotides or residues), and isoelectric point (pH at which net charge is zero,
        crucial for protein solubility and interaction potential).

        Parameters:
        - sequence (str): The biological sequence to analyze.

        Returns:
        - dict: Compositional metrics.
        """
        seq = sequence.upper()

        # GC-content calculation for genomic stability assessment (DNA only)
        if all(c.upper() in 'ATCG' for c in seq):
            gc_content = GC(seq)
        else:
            gc_content = None

        # Molecular weight determination for proteomic mass spectrometry
        mol_weight = molecular_weight(seq)

        # Isoelectric point for protein charge distribution analysis
        if all(c in 'ATCG' for c in seq):
            # DNA sequence: pI not directly applicable
            pi = None
        else:
            # Protein sequence: compute isoelectric point
            ip = IsoelectricPoint(seq)
            pi = ip.pi()

        return {
            'gc_content': gc_content,
            'molecular_weight': mol_weight,
            'isoelectric_point': pi
        }

    def zoonotic_risk_assessment(self, human_seq, animal_seq):
        """
        Assess zoonotic transmission risk based on protein surface charge compatibility.

        This algorithm evaluates the potential for cross-species protein-protein
        interactions by comparing isoelectric points, which correlate with surface
        charge distributions. Similar pI values suggest electrostatic compatibility,
        potentially facilitating receptor binding and interspecies transmission.

        Parameters:
        - human_seq (str): Human protein sequence.
        - animal_seq (str): Animal protein sequence.

        Returns:
        - dict: Risk assessment including pI difference and qualitative risk level.
        """
        # Analyze compositions to obtain isoelectric points
        human_comp = self.analyze_composition(human_seq)
        animal_comp = self.analyze_composition(animal_seq)

        human_pi = human_comp['isoelectric_point']
        animal_pi = animal_comp['isoelectric_point']

        if human_pi is None or animal_pi is None:
            return {'error': 'Isoelectric point not computable for one or both sequences'}

        # Calculate pI difference as a proxy for charge similarity
        pi_difference = abs(human_pi - animal_pi)

        # Risk stratification based on empirical thresholds
        if pi_difference < 0.5:
            risk_level = 'High'
            description = 'Strong electrostatic compatibility suggests elevated zoonotic potential.'
        elif pi_difference < 1.0:
            risk_level = 'Moderate'
            description = 'Moderate charge similarity indicates possible cross-species interactions.'
        else:
            risk_level = 'Low'
            description = 'Dissimilar surface charges reduce likelihood of zoonotic transmission.'

        return {
            'human_pi': human_pi,
            'animal_pi': animal_pi,
            'pi_difference': pi_difference,
            'risk_level': risk_level,
            'description': description
        }