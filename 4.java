public class PhredQualityParser {
    public static int getPhredScore(char asciiChar) {
        return (int) asciiChar - 33;
    }

    public static double getErrorProbability(char asciiChar) {
        int Q = getPhredScore(asciiChar);
        return Math.pow(10, -Q / 10.0);
    }
}