import java.util.*;

public class SingleCellRnaProfiler {

    private final Map<String, Map<String, Integer>> expressionMatrix = new HashMap<>();

    /**
     * Adds transcript count for a given cell barcode and gene identifier.
     */
    public void addExpressionCount(String cellBarcode, String geneId, int count) {
        expressionMatrix
            .computeIfAbsent(cellBarcode, k -> new HashMap<>())
            .put(geneId, count);
    }

    /**
     * Computes mean transcript expression level for a given gene across all sampled cells.
     */
    public double getMeanGeneExpression(String geneId) {
        if (expressionMatrix.isEmpty()) return 0.0;

        int totalCount = 0;
        int cellCount = 0;

        for (Map<String, Integer> cellProfile : expressionMatrix.values()) {
            if (cellProfile.containsKey(geneId)) {
                totalCount += cellProfile.get(geneId);
                cellCount++;
            }
        }

        return cellCount == 0 ? 0.0 : (double) totalCount / cellCount;
    }

    /**
     * Retrieves all cell barcodes exceeding a total transcript threshold.
     */
    public List<String> filterHighQualityCells(int minTotalTranscripts) {
        List<String> validCells = new ArrayList<>();
        for (Map.Entry<String, Map<String, Integer>> entry : expressionMatrix.entrySet()) {
            int total = entry.getValue().values().stream().mapToInt(Integer::intValue).sum();
            if (total >= minTotalTranscripts) {
                validCells.add(entry.getKey());
            }
        }
        return validCells;
    }
}