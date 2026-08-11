import java.util.ArrayList;
import java.util.List;

public class OrfScanner {
    public static List<String> extractORFs(String rna) {
        List<String> orfs = new ArrayList<>();
        for (int i = 0; i <= rna.length() - 3; i++) {
            if (rna.substring(i, i + 3).equals("AUG")) {
                for (int j = i + 3; j <= rna.length() - 3; j += 3) {
                    String codon = rna.substring(j, j + 3);
                    if (codon.equals("UAA") || codon.equals("UAG") || codon.equals("UGA")) {
                        orfs.add(rna.substring(i, j + 3));
                        break;
                    }
                }
            }
        }
        return orfs;
    }
}