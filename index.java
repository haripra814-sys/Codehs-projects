import java.util.HashMap;
import java.util.Map;

public class DNAAnalyzer {

    private final String sequence;

    public DNAAnalyzer(String sequence) {
        this.sequence = sequence.toUpperCase().trim();
    }

    /**
     * Validates if the sequence contains only standard DNA nucleotides (A, T, C, G).
     */
    public boolean isValidDNA() {
        return sequence.matches("[ATCG]+");
    }

    /**
     * Calculates the GC-Content percentage (G + C) / Total Length * 100.
     */
    public double calculateGCContent() {
        if (sequence.isEmpty()) return 0.0;

        long gcCount = sequence.chars()
                .filter(ch -> ch == 'G' || ch == 'C')
                .count();

        return ((double) gcCount / sequence.length()) * 100.0;
    }

    /**
     * Transcribes the DNA sequence into mRNA (replaces Thymine with Uracil).
     */
    public String transcribeToRNA() {
        return sequence.replace('T', 'U');
    }

    /**
     * Counts the occurrence of each nucleotide.
     */
    public Map<Character, Integer> getNucleotideCounts() {
        Map<Character, Integer> counts = new HashMap<>();
        counts.put('A', 0);
        counts.put('T', 0);
        counts.put('C', 0);
        counts.put('G', 0);

        for (char base : sequence.toCharArray()) {
            counts.put(base, counts.getOrDefault(base, 0) + 1);
        }
        return counts;
    }

    public static void main(String[] args) {
        // Example DNA sequence
        String rawSequence = "ATGCGATCGATCGATCGATCGATCGATCGA";
        DNAAnalyzer analyzer = new DNAAnalyzer(rawSequence);

        if (!analyzer.isValidDNA()) {
            System.out.println("Invalid DNA sequence provided.");
            return;
        }

        System.out.println("--- Bioinformatics DNA Analysis ---");
        System.out.println("Original DNA: " + rawSequence);
        System.out.println("Sequence Length: " + rawSequence.length() + " bp");
        System.out.printf("GC Content: %.2f%%\n", analyzer.calculateGCContent());
        System.out.println("RNA Transcription: " + analyzer.transcribeToRNA());
        
        System.out.println("\nNucleotide Counts:");
        analyzer.getNucleotideCounts().forEach((base, count) -> 
            System.out.println(base + ": " + count)
        );
    }
}