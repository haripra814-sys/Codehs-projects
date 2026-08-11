import java.util.HashMap;
import java.util.Map;

public class CodonOptimizationTable {

    private static final Map<Character, String> E_COLI_PREFERRED_CODONS = new HashMap<>();

    static {
        // Preferred high-expression codons in E. coli
        E_COLI_PREFERRED_CODONS.put('A', "GCG");
        E_COLI_PREFERRED_CODONS.put('C', "TGC");
        E_COLI_PREFERRED_CODONS.put('D', "GAT");
        E_COLI_PREFERRED_CODONS.put('E', "GAA");
        E_COLI_PREFERRED_CODONS.put('F', "TTC");
        E_COLI_PREFERRED_CODONS.put('G', "GGC");
        E_COLI_PREFERRED_CODONS.put('H', "CAC");
        E_COLI_PREFERRED_CODONS.put('I', "ATC");
        E_COLI_PREFERRED_CODONS.put('K', "AAA");
        E_COLI_PREFERRED_CODONS.put('L', "CTG");
        E_COLI_PREFERRED_CODONS.put('M', "ATG");
        E_COLI_PREFERRED_CODONS.put('N', "AAC");
        E_COLI_PREFERRED_CODONS.put('P', "CCG");
        E_COLI_PREFERRED_CODONS.put('Q', "CAG");
        E_COLI_PREFERRED_CODONS.put('R', "CGT");
        E_COLI_PREFERRED_CODONS.put('S', "AGC");
        E_COLI_PREFERRED_CODONS.put('T', "ACC");
        E_COLI_PREFERRED_CODONS.put('V', "GTG");
        E_COLI_PREFERRED_CODONS.put('W', "TGG");
        E_COLI_PREFERRED_CODONS.put('Y', "TAC");
    }

    /**
     * Converts a protein sequence into an E. coli codon-optimized DNA sequence.
     */
    public static String backTranslate(String aminoAcids) {
        StringBuilder dnaBuilder = new StringBuilder();
        for (char aa : aminoAcids.toUpperCase().toCharArray()) {
            String codon = E_COLI_PREFERRED_CODONS.getOrDefault(aa, "NNN");
            dnaBuilder.append(codon);
        }
        return dnaBuilder.toString();
    }
}

import java.util.HashMap;
import java.util.Map;

public class KmerFrequencyCounter {
    
    /**
     * Extracts k-mers and their frequency counts from a given DNA string.
     */
    public static Map<String, Integer> getKmerFrequencies(String dna, int k) {
        Map<String, Integer> frequencies = new HashMap<>();
        if (dna == null || k <= 0 || k > dna.length()) {
            return frequencies;
        }

        String sequence = dna.toUpperCase();
        for (int i = 0; i <= sequence.length() - k; i++) {
            String kmer = sequence.substring(i, i + k);
            frequencies.put(kmer, frequencies.getOrDefault(kmer, 0) + 1);
        }

        return frequencies;
    }
}public class PhredQualityParser {
    public static int getPhredScore(char asciiChar) {
        return (int) asciiChar - 33;
    }

    public static double getErrorProbability(char asciiChar) {
        int Q = getPhredScore(asciiChar);
        return Math.pow(10, -Q / 10.0);
    }
}