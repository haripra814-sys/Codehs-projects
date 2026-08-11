import java.util.*;

public class BiotechToolkit {

    /**
     * 1. Restriction Digest: Cuts DNA sequence at a given enzyme recognition site (e.g., EcoRI: GAATTC)
     */
    public static List<String> restrictionDigest(String dna, String site) {
        List<String> fragments = new ArrayList<>();
        int index = 0;
        int matchIndex;
        
        while ((matchIndex = dna.indexOf(site, index)) != -1) {
            fragments.add(dna.substring(index, matchIndex + 1)); // Cuts after first base in site
            index = matchIndex + 1;
        }
        fragments.add(dna.substring(index));
        return fragments;
    }

    /**
     * 2. Primer Melting Temperature (Tm) using Wallace Rule (for sequences < 14 bp) 
     * or Basic Formula: Tm = 64.9 + 41 * (G+C - 16.4) / (A+T+G+C)
     */
    public static double calculateMeltingTemp(String primer) {
        long g = primer.chars().filter(c -> c == 'G').count();
        long c = primer.chars().filter(c -> c == 'C').count();
        long a = primer.chars().filter(c -> c == 'A').count();
        long t = primer.chars().filter(c -> c == 'T').count();
        long len = primer.length();

        if (len == 0) return 0.0;
        if (len < 14) {
            return (a + t) * 2 + (g + c) * 4;
        }
        return 64.9 + 41.0 * ((g + c) - 16.4) / len;
    }

    /**
     * 3. Hamming Distance: Counts point mutation differences between equal-length sequences
     */
    public static int hammingDistance(String seq1, String seq2) {
        if (seq1.length() != seq2.length()) return -1;
        int distance = 0;
        for (int i = 0; i < seq1.length(); i++) {
            if (seq1.charAt(i) != seq2.charAt(i)) {
                distance++;
            }
        }
        return distance;
    }

    /**
     * 4. K-mer Frequency Analysis: Maps k-length sequence counts across a genome
     */
    public static Map<String, Integer> countKmers(String dna, int k) {
        Map<String, Integer> kmerCounts = new HashMap<>();
        for (int i = 0; i <= dna.length() - k; i++) {
            String kmer = dna.substring(i, i + k);
            kmerCounts.put(kmer, kmerCounts.getOrDefault(kmer, 0) + 1);
        }
        return kmerCounts;
    }

    /**
     * 5. Protein Molecular Weight Estimator (g/mol) based on average monoisotopic residues
     */
    public static double estimateProteinWeight(String proteinSingleLetter) {
        Map<Character, Double> weights = Map.ofEntries(
            Map.entry('A', 89.09), Map.entry('R', 174.20), Map.entry('N', 132.12),
            Map.entry('D', 133.10), Map.entry('C', 121.16), Map.entry('E', 147.13),
            Map.entry('Q', 146.15), Map.entry('G', 75.07), Map.entry('H', 155.16),
            Map.entry('I', 131.17), Map.entry('L', 131.17), Map.entry('K', 146.19),
            Map.entry('M', 149.21), Map.entry('F', 165.19), Map.entry('P', 115.13),
            Map.entry('S', 105.09), Map.entry('T', 119.12), Map.entry('W', 204.23),
            Map.entry('Y', 181.19), Map.entry('V', 117.15)
        );

        double totalWeight = 0.0;
        for (char aa : proteinSingleLetter.toUpperCase().toCharArray()) {
            totalWeight += weights.getOrDefault(aa, 0.0);
        }
        return totalWeight > 0 ? totalWeight - (18.015 * (proteinSingleLetter.length() - 1)) : 0.0; // Subtracts water loss from peptide bonds
    }

    public static void main(String[] args) {
        String sampleGenome = "GAATTCATCGATCGAATTCAGCTAGCTA";
        
        System.out.println("--- Extended Biotech Tools ---");
        
        // 1. Restriction Enzyme Cutting
        List<String> fragments = restrictionDigest(sampleGenome, "GAATTC");
        System.out.println("EcoRI Fragments: " + fragments);

        // 2. Primer Melting Temp
        String primer = "ACGTACGTACGT";
        System.out.printf("Primer Melting Temp (%s): %.2f °C\n", primer, calculateMeltingTemp(primer));

        // 3. Hamming Distance Mutation Count
        String wildType = "ATCGATCG";
        String mutant   = "ATGGATCC";
        System.out.println("Hamming Distance (Mutations): " + hammingDistance(wildType, mutant));

        // 4. K-Mer Profiling
        System.out.println("3-mer Counts: " + countKmers(sampleGenome, 3));

        // 5. Protein Weight
        String peptide = "MGGK";
        System.out.printf("Peptide MW (%s): %.2f g/mol\n", peptide, estimateProteinWeight(peptide));
    }
}