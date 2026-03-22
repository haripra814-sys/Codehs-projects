from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

STANFORD_RESOURCES = [
    {"name": "Stanford CS 448A: Computational Biology", "url": "https://cs448a.stanford.edu"},
    {"name": "Stanford Bioinformatics Core", "url": "https://med.stanford.edu/bioinformatics.html"},
    {"name": "BioX at Stanford", "url": "https://biox.stanford.edu"},
    {"name": "Coursera: Genomic Data Science", "url": "https://www.coursera.org/specializations/genomic-data-science"},
]

@app.route("/")
def index():
    return render_template("index.html", resources=STANFORD_RESOURCES)


def compute_kmers(sequence: str, k: int):
    seq = sequence.upper().replace(" ", "").replace("\n", "")
    if k < 1 or k > len(seq):
        return {}
    counts = {}
    for i in range(len(seq) - k + 1):
        kmer = seq[i : i + k]
        counts[kmer] = counts.get(kmer, 0) + 1
    return counts


@app.route("/kmer", methods=["GET", "POST"])
def kmer():
    result = None
    error = None
    if request.method == "POST":
        seq = request.form.get("sequence", "").strip()
        try:
            k = int(request.form.get("k", "3"))
            if not seq:
                raise ValueError("Empty sequence")
            result = compute_kmers(seq, k)
            save_session("k-mer Counter", f"Seq: {seq}, k={k}", f"Counts: {result}")
        except ValueError:
            error = "Enter valid DNA/RNA sequence and integer k."
    return render_template("kmer.html", result=result, error=error)


@app.route("/gc", methods=["GET", "POST"])
def gc():
    gc_pct = None
    error = None
    seq = ""
    if request.method == "POST":
        seq = request.form.get("sequence", "").strip().upper()
        if not seq:
            error = "Enter sequence"
        else:
            valid = all(c in "ACGTU" for c in seq)
            if not valid:
                error = "Sequence contains invalid characters. Use A/C/G/T/U only."
            else:
                gc = seq.count("G") + seq.count("C")
                gc_pct = round(gc / len(seq) * 100, 2)
                save_session("GC Content", seq, f"GC%: {gc_pct}")
    return render_template("gc.html", seq=seq, gc_pct=gc_pct, error=error)


def parse_fasta(text: str):
    sequences = []
    header = None
    seq_chunks = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header:
                sequences.append({"header": header, "sequence": "".join(seq_chunks)})
            header = line[1:].strip()
            seq_chunks = []
        else:
            seq_chunks.append(line)
    if header:
        sequences.append({"header": header, "sequence": "".join(seq_chunks)})
    return sequences


def reverse_complement(seq: str):
    comp = str.maketrans("ACGTUacgtu", "TGCATtgcaa")
    return seq.translate(comp)[::-1]


def translate_dna(seq: str):
    codon_table = {
        'ATA':'I','ATC':'I','ATT':'I','ATG':'M','ACA':'T','ACC':'T','ACG':'T','ACT':'T',
        'AAC':'N','AAT':'N','AAA':'K','AAG':'K','AGC':'S','AGT':'S','AGA':'R','AGG':'R',
        'CTA':'L','CTC':'L','CTG':'L','CTT':'L','CCA':'P','CCC':'P','CCG':'P','CCT':'P',
        'CAC':'H','CAT':'H','CAA':'Q','CAG':'Q','CGA':'R','CGC':'R','CGG':'R','CGT':'R',
        'GTA':'V','GTC':'V','GTG':'V','GTT':'V','GCA':'A','GCC':'A','GCG':'A','GCT':'A',
        'GAC':'D','GAT':'D','GAA':'E','GAG':'E','GGA':'G','GGC':'G','GGG':'G','GGT':'G',
        'TCA':'S','TCC':'S','TCG':'S','TCT':'S','TTC':'F','TTT':'F','TTA':'L','TTG':'L',
        'TAC':'Y','TAT':'Y','TAA':'*','TAG':'*','TGC':'C','TGT':'C','TGA':'*','TGG':'W',
    }
    seq = seq.upper().replace("U", "T")
    aa = []
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        aa.append(codon_table.get(codon, 'X'))
    return ''.join(aa)


def needleman_wunsch(seq1: str, seq2: str, match=1, mismatch=-1, gap=-2):
    seq1 = seq1.upper().replace(" ", "").replace("\n", "")
    seq2 = seq2.upper().replace(" ", "").replace("\n", "")
    n = len(seq1)
    m = len(seq2)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        score[i][0] = gap * i
    for j in range(m + 1):
        score[0][j] = gap * j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match_score = match if seq1[i-1] == seq2[j-1] else mismatch
            score[i][j] = max(
                score[i-1][j-1] + match_score,
                score[i-1][j] + gap,
                score[i][j-1] + gap
            )
    align1, align2 = "", ""
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and score[i][j] == score[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch):
            align1 = seq1[i-1] + align1
            align2 = seq2[j-1] + align2
            i -= 1
            j -= 1
        elif i > 0 and score[i][j] == score[i-1][j] + gap:
            align1 = seq1[i-1] + align1
            align2 = "-" + align2
            i -= 1
        else:
            align1 = "-" + align1
            align2 = seq2[j-1] + align2
            j -= 1
    return align1, align2, score[n][m]


def find_motifs(sequence: str, motif: str):
    seq = sequence.upper().replace(" ", "").replace("\n", "")
    motif = motif.upper().replace(" ", "").replace("\n", "")
    positions = []
    for i in range(len(seq) - len(motif) + 1):
        if seq[i:i+len(motif)] == motif:
            positions.append(i + 1)  # 1-based
    return positions


def init_db():
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tool TEXT,
        input_data TEXT,
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()


def save_session(tool: str, input_data: str, result: str):
    init_db()
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute("INSERT INTO sessions (tool, input_data, result) VALUES (?, ?, ?)", (tool, input_data, result))
    conn.commit()
    conn.close()


def get_sessions():
    init_db()
    conn = sqlite3.connect('sessions.db')
    c = conn.cursor()
    c.execute("SELECT id, tool, input_data, result, timestamp FROM sessions ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows


@app.route("/fasta", methods=["GET", "POST"])
def fasta():
    data = None
    error = None
    if request.method == "POST":
        text = request.form.get("fasta_text", "").strip()
        if not text:
            error = "Provide FASTA data."
        else:
            seqs = parse_fasta(text)
            if not seqs:
                error = "No FASTA records found."
            else:
                for entry in seqs:
                    seq = entry['sequence'].upper().replace(' ', '').replace('\n', '')
                    entry['length'] = len(seq)
                    entry['gc'] = round((seq.count('G') + seq.count('C')) / max(len(seq), 1) * 100, 2)
                    entry['rev_comp'] = reverse_complement(seq)
                    entry['translation'] = translate_dna(seq)
                data = seqs
                save_session("FASTA Analyzer", text, f"Processed {len(seqs)} sequences")
    return render_template('fasta.html', data=data, error=error)


@app.route("/align", methods=["GET", "POST"])
def align():
    result = None
    error = None
    seq1 = ""
    seq2 = ""
    if request.method == "POST":
        seq1 = request.form.get("seq1", "").strip()
        seq2 = request.form.get("seq2", "").strip()
        if not seq1 or not seq2:
            error = "Provide both sequences."
        else:
            try:
                align1, align2, score = needleman_wunsch(seq1, seq2)
                result = {"align1": align1, "align2": align2, "score": score}
                save_session("Alignment", f"Seq1: {seq1}\nSeq2: {seq2}", f"Score: {score}")
            except Exception as e:
                error = f"Alignment error: {str(e)}"
    return render_template("align.html", result=result, error=error, seq1=seq1, seq2=seq2)


@app.route("/motif", methods=["GET", "POST"])
def motif():
    positions = None
    error = None
    seq = ""
    motif_str = ""
    if request.method == "POST":
        seq = request.form.get("sequence", "").strip()
        motif_str = request.form.get("motif", "").strip()
        if not seq or not motif_str:
            error = "Provide sequence and motif."
        else:
            positions = find_motifs(seq, motif_str)
            save_session("Motif Search", f"Seq: {seq}\nMotif: {motif_str}", f"Positions: {positions}")
    return render_template("motif.html", positions=positions, error=error, seq=seq, motif=motif_str)


@app.route("/sessions")
def sessions():
    data = get_sessions()
    return render_template("sessions.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
