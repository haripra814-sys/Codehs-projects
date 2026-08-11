import java.util.*;

public class BiotechSuite {

    // 1. FASTQ Quality Score Parser (Converts ASCII Phred+33 to Error Probabilities)
    public static class FastqParser {
        public static double[] phredToErrorProbability(String qualityString) {
            double[] probabilities = new double[qualityString.length()];
            for (int i = 0; i < qualityString.length(); i++) {
                int phredScore = (int) qualityString.charAt(i) - 33;
                probabilities[i] = Math.pow(10, -phredScore / 10.0);
            }
            return probabilities;
        }
    }

    // 2. Open Reading Frame (ORF) Finder
    public static class OrfFinder {
        public static List<String> findORFs(String rnaSequence) {
            List<String> orfs = new ArrayList<>();
            for (int i = 0; i <= rnaSequence.length() - 3; i++) {
                if (rnaSequence.substring(i, i + 3).equals("AUG")) {
                    for (int j = i + 3; j <= rnaSequence.length() - 3; j += 3) {
                        String codon = rnaSequence.substring(j, j + 3);
                        if (codon.equals("UAA") || codon.equals("UAG") || codon.equals("UGA")) {
                            orfs.add(rnaSequence.substring(i, j + 3));
                            break;
                        }
                    }
                }
            }
            return orfs;
        }
    }

    // 3. Kyte-Doolittle Hydrophobicity Index Calculator
    public static class HydrophobicityCalculator {
        private static final Map<Character, Double> KD_SCALE = Map.ofEntries(
            Map.entry('I', 4.5), Map.entry('V', 4.2), Map.entry('L', 3.8), Map.entry('F', 2.8),
            Map.entry('C', 2.5), Map.entry('M', 1.9), Map.entry('A', 1.8), Map.entry('G', -0.4),
            Map.entry('T', -0.7), Map.entry('S', -0.8), Map.entry('W', -0.9), Map.entry('Y', -1.3),
            Map.entry('P', -1.6), Map.entry('H', -3.2), Map.entry('E', -3.5), Map.entry('Q', -3.5),
            Map.entry('D', -3.5), Map.entry('N', -3.5), Map.entry('K', -3.9), Map.entry('R', -4.5)
        );

        public static double calculateGRAVY(String protein) {
            double sum = 0;
            int count = 0;
            for (char aa : protein.toUpperCase().toCharArray()) {
                if (KD_SCALE.containsKey(aa)) {
                    sum += KD_SCALE.get(aa);
                    count++;
                }
            }
            return count == 0 ? 0 : sum / count;
        }
    }

    // 4. PCR Primer Design Checker
    public static class PrimerChecker {
        public static boolean isValidPrimer(String primer) {
            if (primer.length() < 18 || primer.length() > 24) return false;
            long gcCount = primer.chars().filter(c -> c == 'G' || c == 'C').count();
            double gcContent = (double) gcCount / primer.length();
            char lastBase = primer.charAt(primer.length() - 1);
            boolean gcClamp = (lastBase == 'G' || lastBase == 'C');
            return gcContent >= 0.40 && gcContent <= 0.60 && gcClamp;
        }
    }

    // 5. Isoelectric Point (pI) Estimator for Peptides
    public static class IsoelectricPointCalculator {
        public static double estimatePI(String peptide) {
            double netCharge;
            double pH = 0.0;
            while (pH <= 14.0) {
                netCharge = calculateNetCharge(peptide, pH);
                if (netCharge <= 0) break;
                pH += 0.01;
            }
            return pH;
        }

        private static double calculateNetCharge(String seq, double pH) {
            double charge = 1.0 / (1.0 + Math.pow(10, pH - 9.69)) - 1.0 / (1.0 + Math.pow(10, 2.34 - pH));
            for (char aa : seq.toUpperCase().toCharArray()) {
                switch (aa) {
                    case 'D' -> charge -= 1.0 / (1.0 + Math.pow(10, 3.86 - pH));
                    case 'E' -> charge -= 1.0 / (1.0 + Math.pow(10, 4.25 - pH));
                    case 'H' -> charge += 1.0 / (1.0 + Math.pow(10, pH - 6.00));
                    case 'K' -> charge += 1.0 / (1.0 + Math.pow(10, pH - 10.51));
                    case 'R' -> charge += 1.0 / (1.0 + Math.pow(10, pH - 12.48));
                    case 'Y' -> charge -= 1.0 / (1.0 + Math.pow(10, 10.07 - pH));
                    case 'C' -> charge -= 1.0 / (1.0 + Math.pow(10, 8.33 - pH));
                }
            }
            return charge;
        }
    }

    // 6. CpG Island Detector (Genomic Methylation Regions)
    public static class CpGIslandDetector {
        public static boolean isCpGIsland(String dnaWindow) {
            long c = dnaWindow.chars().filter(ch -> ch == 'C').count();
            long g = dnaWindow.chars().filter(ch -> ch == 'G').count();
            double gcRatio = (double) (c + g) / dnaWindow.length();

            int cgCount = 0;
            for (int i = 0; i < dnaWindow.length() - 1; i++) {
                if (dnaWindow.charAt(i) == 'C' && dnaWindow.charAt(i + 1) == 'G') cgCount++;
            }

            double expectedCG = ((double) c * g) / dnaWindow.length();
            double observedToExpected = expectedCG == 0 ? 0 : (double) cgCount / expectedCG;

            return gcRatio > 0.50 && observedToExpected > 0.60;
        }
    }

    // 7. Levenshtein Distance (Indel-Aware Sequence Comparison)
    public static class SequenceDistance {
        public static int levenshteinDistance(String a, String b) {
            int[][] dp = new int[a.length() + 1][b.length() + 1];
            for (int i = 0; i <= a.length(); i++) dp[i][0] = i;
            for (int j = 0; j <= b.length(); j++) dp[0][j] = j;

            for (int i = 1; i <= a.length(); i++) {
                for (int j = 1; j <= b.length(); j++) {
                    int cost = (a.charAt(i - 1) == b.charAt(j - 1)) ? 0 : 1;
                    dp[i][j] = Math.min(Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1), dp[i - 1][j - 1] + cost);
                }
            }
            return dp[a.length()][b.length()];
        }
    }

    // 8. FASTA Record Parser
    public static class FastaRecord {
        public final String header;
        public final String sequence;

        public FastaRecord(String rawFasta) {
            String[] lines = rawFasta.split("\n", 2);
            this.header = lines[0].startsWith(">") ? lines[0].substring(1).trim() : "Unknown";
            this.sequence = lines.length > 1 ? lines[1].replaceAll("\\s+", "").toUpperCase() : "";
        }
    }

    // 9. Codon Adaptation Index (CAI) Simplification
    public static class CodonUsageAnalyzer {
        public static Map<String, Double> calculateCodonFrequencies(String rnaSeq) {
            Map<String, Integer> counts = new HashMap<>();
            int totalCodons = 0;
            for (int i = 0; i <= rnaSeq.length() - 3; i += 3) {
                String codon = rnaSeq.substring(i, i + 3);
                counts.put(codon, counts.getOrDefault(codon, 0) + 1);
                totalCodons++;
            }
            Map<String, Double> frequencies = new HashMap<>();
            for (Map.Entry<String, Integer> entry : counts.entrySet()) {
                frequencies.put(entry.getKey(), (double) entry.getValue() / totalCodons);
            }
            return frequencies;
        }
    }

    // 10. Enzyme Michaelis-Menten Kinetics Simulator
    public static class MichaelisMentenSimulator {
        public static double calculateReactionVelocity(double vMax, double km, double substrateConc) {
            return (vMax * substrateConc) / (km + substrateConc);
        }
    }

    public static void main(String[] args) {
        System.out.println("=== 10-in-1 Biotech Suite Executed Successfully ===");
        System.out.println("1. FASTQ Error (Scores 'I'): " + FastqParser.phredToErrorProbability("I")[0]);
        System.out.println("2. ORFs Found: " + OrfFinder.findORFs("AUGGCCUAA"));
        System.out.println("3. GRAVY Score: " + HydrophobicityCalculator.calculateGRAVY("IVLFC"));
        System.out.println("4. Valid Primer: " + PrimerChecker.isValidPrimer("ATGCGATCGATCGATCGATC"));
        System.out.println("5. Estimated pI: " + IsoelectricPointCalculator.estimatePI("MGGKEDH"));
        System.out.println("6. Is CpG Island: " + CpGIslandDetector.isCpGIsland("CGCGCGCGCGCGCGCGCGCG"));
        System.out.println("7. Levenshtein Distance: " + SequenceDistance.levenshteinDistance("AGCT", "AATC"));
        
        FastaRecord fasta = new FastaRecord(">Seq1\nATGC\nGGTC");
        System.out.println("8. FASTA Header: " + fasta.header + " | Length: " + fasta.sequence.length());
        System.out.println("9. Codon Frequency: " + CodonUsageAnalyzer.calculateCodonFrequencies("AUGGCCUAA"));
        System.out.println("10. Reaction Velocity (vMax=100, Km=2, [S]=5): " + MichaelisMentenSimulator.calculateReactionVelocity(100, 2, 5));
    }
}