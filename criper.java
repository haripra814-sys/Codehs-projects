import java.util.ArrayList;
import java.util.List;

public class CrisprTargetFinder {

    public record TargetSite(int startIndex, int endIndex, String guideRna, String pam) {
        @Override
        public String toString() {
            return String.format("Pos %d-%d | gRNA (20bp): %s | PAM: %s", startIndex, endIndex, guideRna, pam);
        }
    }

    /**
     * Finds SpCas9 target sites (20bp target + NGG PAM sequence).
     */
    public static List<TargetSite> findCas9Targets(String dna) {
        List<TargetSite> targets = new ArrayList<>();
        if (dna == null || dna.length() < 23) {
            return targets;
        }

        String sequence = dna.toUpperCase();
        // Look for NGG motif starting at index 20
        for (int i = 20; i < sequence.length() - 2; i++) {
            if (sequence.charAt(i + 1) == 'G' && sequence.charAt(i + 2) == 'G') {
                String guideRna = sequence.substring(i - 20, i);
                String pam = sequence.substring(i, i + 3);
                targets.add(new TargetSite(i - 20, i + 3, guideRna, pam));
            }
        }
        return targets;
    }
}