import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class FastaFileReader {
    public static Map<String, String> readFasta(String filePath) throws IOException {
        Map<String, String> sequences = new HashMap<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            String currentHeader = null;
            StringBuilder currentSeq = new StringBuilder();

            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (line.startsWith(">")) {
                    if (currentHeader != null) {
                        sequences.put(currentHeader, currentSeq.toString());
                    }
                    currentHeader = line.substring(1);
                    currentSeq = new StringBuilder();
                } else {
                    currentSeq.append(line.toUpperCase());
                }
            }
            if (currentHeader != null) {
                sequences.put(currentHeader, currentSeq.toString());
            }
        }
        return sequences;
    }
}