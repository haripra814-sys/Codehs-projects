public class CpGIslandFinder {
    public static boolean isCpGIsland(String sequenceWindow) {
        int length = sequenceWindow.length();
        if (length < 200) return false;

        long cCount = sequenceWindow.chars().filter(c -> c == 'C').count();
        long gCount = sequenceWindow.chars().filter(c -> c == 'G').count();
        double gcPercent = (double) (cCount + gCount) / length;

        int cgPairs = 0;
        for (int i = 0; i < length - 1; i++) {
            if (sequenceWindow.charAt(i) == 'C' && sequenceWindow.charAt(i + 1) == 'G') {
                cgPairs++;
            }
        }

        double expectedCg = ((double) cCount * gCount) / length;
        double obsToExpRatio = expectedCg == 0 ? 0 : (double) cgPairs / expectedCg;

        return gcPercent >= 0.50 && obsToExpRatio >= 0.60;
    }
}