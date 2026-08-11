public class PcrPrimerValidator {
    public static boolean validatePrimer(String primer) {
        if (primer == null || primer.length() < 18 || primer.length() > 24) {
            return false;
        }

        long gcCount = primer.chars().filter(c -> c == 'G' || c == 'C').count();
        double gcPercent = (double) gcCount / primer.length();

        char lastChar = primer.charAt(primer.length() - 1);
        boolean hasGcClamp = (lastChar == 'G' || lastChar == 'C');

        return gcPercent >= 0.40 && gcPercent <= 0.60 && hasGcClamp;
    }
}