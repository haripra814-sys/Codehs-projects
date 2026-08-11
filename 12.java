import java.util.Map;

public class MolecularWeightCalculator {
    private static final Map<Character, Double> AA_WEIGHTS = Map.ofEntries(
        Map.entry('A', 89.09), Map.entry('R', 174.20), Map.entry('N', 132.12),
        Map.entry('D', 133.10), Map.entry('C', 121.16), Map.entry('E', 147.13),
        Map.entry('Q', 146.15), Map.entry('G', 75.07), Map.entry('H', 155.16),
        Map.entry('I', 131.17), Map.entry('L', 131.17), Map.entry('K', 146.19),
        Map.entry('M', 149.21), Map.entry('F', 165.19), Map.entry('P', 115.13),
        Map.entry('S', 105.09), Map.entry('T', 119.12), Map.entry('W', 204.23),
        Map.entry('Y', 181.19), Map.entry('V', 117.15)
    );

    public static double getPeptideWeight(String peptide) {
        double weight = 0.0;
        int length = 0;
        for (char aa : peptide.toUpperCase().toCharArray()) {
            if (AA_WEIGHTS.containsKey(aa)) {
                weight += AA_WEIGHTS.get(aa);
                length++;
            }
        }
        return length > 0 ? weight - (18.015 * (length - 1)) : 0.0;
    }
}