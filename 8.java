public class IsoelectricPointEstimator {
    public static double estimatePI(String sequence) {
        double minPh = 0.0;
        double maxPh = 14.0;
        double precision = 0.01;

        while ((maxPh - minPh) > precision) {
            double midPh = minPh + (maxPh - minPh) / 2.0;
            double charge = calculateNetCharge(sequence, midPh);

            if (charge > 0) {
                minPh = midPh;
            } else {
                maxPh = midPh;
            }
        }
        return (minPh + maxPh) / 2.0;
    }

    private static double calculateNetCharge(String seq, double pH) {
        double charge = 1.0 / (1.0 + Math.pow(10, pH - 9.69)) - 1.0 / (1.0 + Math.pow(10, 2.34 - pH));
        for (char aa : seq.toUpperCase().toCharArray()) {
            switch (aa) {
                case 'D' -> charge -= 1.0 / (1.0 + Math.pow(10, 3.86 - pH));
                case 'E' -> charge -= 1.0 / (1.0 + Math.pow(10, 4.25 - pH));
                case 'H' -> charge += 1.0 / (1.0 + Math.pow(10, pH - 6.00));
                case 'K' -> charge += 1.0 / (1.0 + Math.pow(10, pH - 10.51));
                case 'R' -> charge += 1.0 / (1.0 + Math.pow(10, pH - 12.48));
                case 'C' -> charge -= 1.0 / (1.0 + Math.pow(10, 8.33 - pH));
                case 'Y' -> charge -= 1.0 / (1.0 + Math.pow(10, 10.07 - pH));
            }
        }
        return charge;
    }
}