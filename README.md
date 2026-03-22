# Stanford Bioinformatics Web Tool (Python only)

A small Flask web app for college bioinformatics students (Stanford-focused resources).

## Features
- Home page with curated Stanford bioinformatics links
- k-mer counter (user-provided DNA/RNA sequence)
- GC-content calculator
- FASTA parser + per-record stats (length, GC, reverse complement, protein translation)
- Sequence alignment (Needleman-Wunsch algorithm)
- Motif search in sequences
- Saved analysis sessions (SQLite database)

## Setup
1. Create and activate virtual environment:
   - `python -m venv venv`
   - `venv\\Scripts\\activate` (Windows)
2. Install requirements: `pip install -r requirements.txt`
3. Run app: `python app.py`
4. Open `http://127.0.0.1:5000` in browser

## Extend
- Add sequence alignment tools (Needleman-Wunsch)
- Integrate Biopython and gene annotation
- Add user accounts, saved projects, tutorials
