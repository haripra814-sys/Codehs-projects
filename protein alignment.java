import java.util.Arrays;

public class SequenceAligner {

    private final int matchScore;
    private final int mismatchPenalty;
    private final int gapPenalty;

    public SequenceAligner(int matchScore, int mismatchPenalty, int gapPenalty) {
        this.matchScore = matchScore;
        this.mismatchPenalty = mismatchPenalty;
        this.gapPenalty = gapPenalty;
    }

    /**
     * Aligns two DNA sequences using the Needleman-Wunsch algorithm.
     */
    public AlignmentResult align(String seq1, String seq2) {
        int n = seq1.length();
        int m = seq2.length();
        int[][] scoreTable = new int[n + 1][m + 1];

        // Initialize grid boundaries with gap penalties
        for (int i = 0; i <= n; i++) scoreTable[i][0] = i * gapPenalty;
        for (int j = 0; j <= m; j++) scoreTable[0][j] = j * gapPenalty;

        // Fill dynamic programming matrix
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                int match = scoreTable[i - 1][j - 1] + 
                    (seq1.charAt(i - 1) == seq2.charAt(j - 1) ? matchScore : mismatchPenalty);
                int delete = scoreTable[i - 1][j] + gapPenalty;
                int insert = scoreTable[i][j - 1] + gapPenalty;

                scoreTable[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }

        // Traceback to build optimal aligned strings
        StringBuilder aligned1 = new StringBuilder();
        StringBuilder aligned2 = new StringBuilder();
        int i = n, j = m;

        while (i > 0 || j > 0) {
            if (i > 0 && j > 0 && scoreTable[i][j] == scoreTable[i - 1][j - 1] + 
                    (seq1.charAt(i - 1) == seq2.charAt(j - 1) ? matchScore : mismatchPenalty)) {
                aligned1.append(seq1.charAt(i - 1));
                aligned2.append(seq2.charAt(j - 1));
                i--;
                j--;
            } else if (i > 0 && scoreTable[i][j] == scoreTable[i - 1][j] + gapPenalty) {
                aligned1.append(seq1.charAt(i - 1));
                aligned2.append('-');
                i--;
            } else {
                aligned1.append('-');
                aligned2.append(seq2.charAt(j - 1));
                j--;
            }
        }

        return new AlignmentResult(
            aligned1.reverse().toString(),
            aligned2.reverse().toString(),
            scoreTable[n][m]
        );
    }

    public record AlignmentResult(String alignedSeq1, String alignedSeq2, int score) {
        @Override
        public String toString() {
            return String.format("Alignment Score: %d\nSeq 1: %s\nSeq 2: %s", score, alignedSeq1, alignedSeq2);
        }
    }

    public static void main(String[] args) {
        SequenceAligner aligner = new SequenceAligner(1, -1, -2); // Match = +1, Mismatch = -1, Gap = -2

        String seqA = "GATTACA";
        String seqB = "GCATGCU".replace('U', 'A');

        System.out.println("=== Needleman-Wunsch Sequence Alignment ===");
        System.out.println(aligner.align(seqA, seqB));
    }
}