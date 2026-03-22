"""
BioCross-Alpha Flask Backend Server
====================================

This Flask application serves as the web interface for BioCross-Alpha, a
computational biology platform for analyzing human-animal biological interactions.
It integrates the BioAnalyzer engine to provide RESTful API endpoints for sequence
analysis, enabling real-time genomic insights in a user-friendly web environment.

Key Features:
- RESTful API for sequence alignment and composition analysis
- Error handling for invalid nucleotide sequences
- Integration with Jinja2 templating for dynamic UI rendering

Author: Senior Bioinformatics Engineer
Date: March 21, 2026
"""

from flask import Flask, render_template, request, jsonify
from bio_logic import BioAnalyzer

# Initialize Flask application instance
app = Flask(__name__)

# Instantiate the core bioinformatics analyzer
analyzer = BioAnalyzer()

@app.route('/')
def index():
    """
    Render the main dashboard interface.

    This route serves the primary HTML template, providing the user interface
    for inputting genomic sequences and visualizing analysis results.
    """
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    API endpoint for performing comprehensive sequence analysis.

    Accepts POST requests with JSON payload containing human and animal sequences.
    Performs sequence alignment, compositional analysis, and zoonotic risk assessment.
    Returns detailed JSON report with all computed metrics.

    Expected JSON payload:
    {
        "human_seq": "ATCG...",
        "animal_seq": "ATCG..."
    }

    Returns:
    - JSON object with alignment, compositions, and risk assessment
    - Error responses for invalid inputs
    """
    try:
        # Parse incoming JSON data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        human_seq = data.get('human_seq', '').strip()
        animal_seq = data.get('animal_seq', '').strip()

        # Validate presence of sequences
        if not human_seq or not animal_seq:
            return jsonify({'error': 'Both human and animal sequences are required'}), 400

        # Validate amino acid composition (only standard amino acids allowed)
        valid_amino_acids = set('ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy')
        if not all(c in valid_amino_acids for c in human_seq):
            return jsonify({'error': 'Invalid characters in human sequence. Only standard amino acids (A,C,D,E,F,G,H,I,K,L,M,N,P,Q,R,S,T,V,W,Y) allowed.'}), 400
        if not all(c in valid_amino_acids for c in animal_seq):
            return jsonify({'error': 'Invalid characters in animal sequence. Only standard amino acids (A,C,D,E,F,G,H,I,K,L,M,N,P,Q,R,S,T,V,W,Y) allowed.'}), 400

        # Perform bioinformatics analyses
        alignment_result = analyzer.align_sequences(human_seq, animal_seq)
        human_composition = analyzer.analyze_composition(human_seq)
        animal_composition = analyzer.analyze_composition(animal_seq)
        zoonotic_risk = analyzer.zoonotic_risk_assessment(human_seq, animal_seq)

        # Compile comprehensive analysis report
        analysis_report = {
            'alignment': alignment_result,
            'human_composition': human_composition,
            'animal_composition': animal_composition,
            'zoonotic_risk': zoonotic_risk
        }

        return jsonify(analysis_report)

    except Exception as e:
        # Handle unexpected errors gracefully
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Run the Flask development server with debug mode enabled
    app.run(debug=True, host='0.0.0.0', port=5000)