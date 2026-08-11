import java.util.ArrayList;
import java.util.List;

public class GenomicVariantDetector {

    public enum VariantType {
        TRANSITION,    // Purine <-> Purine (A<->G) or Pyrimidine <-> Pyrimidine (C<->T)
        TRANSVERSION,  // Purine <-> Pyrimidine (A/G <-> C/T)
        INDEL,         // Insertion or Deletion
        MATCH
    }

    public record Variant(int position, char referenceBase, char sampleBase, VariantType type) {
        @Override
        public String toString() {
            return String.format("Pos %d: %c -> %c [%s]", position, referenceBase, sampleBase, type);
        }
    }

    /**
     * Detects SNPs and point mutations between a reference and sample DNA sequence.
     */
    public static List<Variant> detectVariants(String reference, String sample) {
        List<Variant> variants = new ArrayList<>();
        int minLength = Math.min(reference.length(), sample.length());

        for (int i = 0; i < minLength; i++) {
            char ref = Character.toUpperCase(reference.charAt(i));
            char sam = Character.toUpperCase(sample.charAt(i));

            if (ref != sam) {
                VariantType type = classifyMutation(ref, sam);
                variants.add(new Variant(i + 1, ref, sam, type));
            }
        }
        return variants;
    }

    /**
     * Classifies single nucleotide mutations as Transitions or Transversions.
     */
    private static VariantType classifyMutation(char ref, char sam) {
        boolean refPurine = (ref == 'A' || ref == 'G');
        boolean samPurine = (sam == 'A' || sam == 'G');

        // If both are purines or both are pyrimidines, it's a Transition
        if (refPurine == samPurine) {
            return VariantType.TRANSITION;
        } else {
            return VariantType.TRANSVERSION;
        }
    }

    public static void main(String[] args) {
        // Example Reference vs. Patient DNA Sequence
        String referenceGenome = "ATGCGATCGATCGATCGATCGATC";
        String patientGenome   = "ATGCGGTCAATCGACCGATCGATC";

        System.out.println("=== Genomic Variant & SNP Detector ===");
        System.out.println("Ref:    " + referenceGenome);
        System.out.println("Sample: " + patientGenome);
        System.out.println("\nDetected Variants:");

        List<Variant> variants = detectVariants(referenceGenome, patientGenome);
        
        if (variants.isEmpty()) {
            System.out.println("No variants detected. Sequences are identical.");
        } else {
            int transitions = 0;
            int transversions = 0;

            for (Variant v : variants) {
                System.out.println(v);
                if (v.type() == VariantType.TRANSITION) transitions++;
                if (v.type() == VariantType.TRANSVERSION) transversions++;
            }

            System.out.println("\nVariant Summary:");
            System.out.println("Total SNPs: " + variants.size());
            System.out.println("Transitions: " + transitions);
            System.out.println("Transversions: " + transversions);
            System.out.printf("Ti/Tv Ratio: %.2f\n", (transversions > 0 ? (double) transitions / transversions : 0.0));
        }
    }
}