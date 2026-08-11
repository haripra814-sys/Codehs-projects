import java.util.*;

public class AdvancedBioinformaticsPipeline {

    private static final Map<String, String> CODON_TABLE = new HashMap<>();

    static {
        // Standard genetic code mapping (Codon -> Amino Acid symbol)
        CODON_TABLE.put("AUG", "Met (Start)");
        CODON_TABLE.put("UUU", "Phe"); CODON_TABLE.put("UUC", "Phe");
        CODON_TABLE.put("UUA", "Leu"); CODON_TABLE.put("UUG", "Leu");
        CODON_TABLE.put("CUU", "Leu"); CODON_TABLE.put("CUC", "Leu");
        CODON_TABLE.put("CUA", "Leu"); CODON_TABLE.put("CUG", "Leu");
        CODON_TABLE.put("GGU", "Gly"); CODON_TABLE.put("GGC", "Gly");
        CODON_TABLE.put("GGA", "Gly"); CODON_TABLE.put("GGG", "Gly");
        CODON_TABLE.put("UAA", "STOP"); CODON_TABLE.put("UAG", "STOP"); CODON_TABLE.put("UGA", "STOP");
    }

    private final String dnaSequence;

    public AdvancedBioinformaticsPipeline(String dnaSequence) {
        this.dnaSequence = dnaSequence.toUpperCase().replaceAll("\\s+", "");
    }

    /**
     * Generates the reverse complement strand (5' to 3' orientation).
     */
    public String getReverseComplement() {
        StringBuilder builder = new StringBuilder();
        for (int i = dnaSequence.length() - 1; i >= 0; i--) {
            char base = dnaSequence.charAt(i);
            switch (base) {
                case 'A' -> builder.append('T');
                case 'T' -> builder.append('A');
                case 'C' -> builder.append('G');
                case 'G' -> builder.append('C');
                default -> builder.append('N');
            }
        }
        return builder.toString();
    }

    /**
     * Transcribes DNA to mRNA.
     */
    public String transcribeToRNA() {
        return dnaSequence.replace('T', 'U');
    }

    /**
     * Translates mRNA into an Amino Acid chain until a STOP codon is met.
     */
    public List<String> translateRNA(String rna) {
        List<String> aminoAcids = new ArrayList<>();
        for (int i = 0; i <= rna.length() - 3; i += 3) {
            String codon = rna.substring(i, i + 3);
            String aminoAcid = CODON_TABLE.getOrDefault(codon, "Unknown");
            
            aminoAcids.add(aminoAcid);
            if ("STOP".equals(aminoAcid)) {
                break;
            }
        }
        return aminoAcids;
    }

    /**
     * Simulates a single point mutation at a specific position.
     */
    public String introducePointMutation(int index, char newBase) {
        if (index < 0 || index >= dnaSequence.length()) return dnaSequence;
        char[] chars = dnaSequence.toCharArray();
        chars[index] = Character.toUpperCase(newBase);
        return new String(chars);
    }

    public static void main(String[] args) {
        String sampleDNA = "ATGGCCGGTGGTUAA".replace('U', 'T'); // Example gene sequence starting with ATG (Start codon)
        
        AdvancedBioinformaticsPipeline pipeline = new AdvancedBioinformaticsPipeline(sampleDNA);

        System.out.println("=== Advanced Biotech Analysis ===");
        System.out.println("5' -> 3' DNA:         " + sampleDNA);
        System.out.println("Reverse Complement:   " + pipeline.getReverseComplement());
        
        String rna = pipeline.transcribeToRNA();
        System.out.println("mRNA Sequence:        " + rna);
        
        List<String> protein = pipeline.translateRNA(rna);
        System.out.println("Translated Protein:   " + String.join(" - ", protein));

        String mutated = pipeline.introducePointMutation(3, 'C');
        System.out.println("Mutated DNA (Pos 3):  " + mutated);
    }
}