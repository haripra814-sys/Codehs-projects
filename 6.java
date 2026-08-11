import java.util.Map;

public class HydrophobicityGRAVY {
    private static final Map<Character, Double> KD_SCALE = Map.ofEntries(
        Map.entry('I', 4.5), Map.entry('V', 4.2), Map.entry('L', 3.8), Map.entry('F', 2.8),
        Map.entry('C', 2.5), Map.entry('M', 1.9), Map.entry('A', 1.8), Map.entry('G', -0.4),
        Map.entry('T', -0.7), Map.entry('S', -0.8), Map.entry('W', -0.9), Map.entry('Y', -1.3),
        Map.entry('P', -1.6), Map.entry('H', -3.2), Map.entry('E', -3.5), Map.entry('Q', -3.5),
        Map.entry('D', -3.5), Map.entry('N', -3.5), Map.entry('K', -3.9), Map.entry('R', -4.5)
    );

    public static double calculateGRAVY(String proteinSequence) {
        double totalScore = 0.0;
        int validResidues = 0;

        for (char aa : proteinSequence.toUpperCase().toCharArray()) {
            if (KD_SCALE.containsKey(aa)) {
                totalScore += KD_SCALE.get(aa);
                validResidues++;
            }
        }
        return validResidues == 0 ? 0.0 : totalScore / validResidues;
    }
}