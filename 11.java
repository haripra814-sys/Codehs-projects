public class LevenshteinDistance {
    public static int compute(String seq1, String seq2) {
        int[][] dp = new int[seq1.length() + 1][seq2.length() + 1];

        for (int i = 0; i <= seq1.length(); i++) dp[i][0] = i;
        for (int j = 0; j <= seq2.length(); j++) dp[0][j] = j;

        for (int i = 1; i <= seq1.length(); i++) {
            for (int j = 1; j <= seq2.length(); j++) {
                int cost = (seq1.charAt(i - 1) == seq2.charAt(j - 1)) ? 0 : 1;
                dp[i][j] = Math.min(
                    Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1),
                    dp[i - 1][j - 1] + cost
                );
            }
        }
        return dp[seq1.length()][seq2.length()];
    }
}