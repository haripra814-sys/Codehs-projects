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