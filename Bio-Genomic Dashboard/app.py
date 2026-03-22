"""
PhyloShield Flask Backend
=========================

This module implements the web server component of the PhyloShield DNA Analysis Platform.
The Flask application provides RESTful API endpoints for genomic analysis and serves
the laboratory dashboard frontend.

Architecture:
- REST API: /analyze endpoint for sequence analysis
- Static File Serving: CSS, JavaScript, and assets
- Template Rendering: HTML dashboard with embedded scientific documentation

Security Considerations:
- Input validation for DNA sequences
- Error handling for malformed requests
- CORS enabled for cross-origin requests (if needed)

Dependencies: Flask, Biopython, Pandas
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from genomics_engine import GenomicsEngine
import os
import re

# Initialize Flask application
app = Flask(__name__,
            template_folder='.',
            static_folder='static')

# Initialize the genomics computation engine
genomics_engine = GenomicsEngine()

def validate_dna_sequence(sequence: str) -> bool:
    """
    Validate DNA sequence format.

    Ensures the input contains only valid DNA nucleotides (A, T, G, C)
    and is of reasonable length for analysis.

    Parameters:
    -----------
    sequence : str
        DNA sequence to validate

    Returns:
    --------
    bool
        True if valid, False otherwise
    """
    if not sequence or len(sequence) == 0:
        return False

    # Check for valid nucleotides only (case-insensitive)
    valid_pattern = re.compile(r'^[ATGCatgc\s]*$')
    if not valid_pattern.match(sequence):
        return False

    # Remove whitespace and check minimum length
    clean_seq = re.sub(r'\s+', '', sequence.upper())
    return len(clean_seq) >= 10  # Minimum 10 nucleotides for meaningful analysis

@app.route('/')
def index():
    """
    Serve the main laboratory dashboard.

    Returns the HTML template for the PhyloShield interface,
    including sequence input forms and visualization components.
    """
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sequences():
    """
    API endpoint for DNA sequence analysis.

    Accepts POST requests with JSON payload containing:
    - human_sequence: str (DNA sequence)
    - animal_sequence: str (DNA sequence)
    - gas_level: float (MQ-135 gas concentration in ppm)

    Returns JSON response with comprehensive analysis report.

    Request Format:
    ---------------
    POST /analyze
    Content-Type: application/json

    {
        "human_sequence": "ATCGATCG...",
        "animal_sequence": "GCTAGCTA...",
        "gas_level": 15.5
    }

    Response Format:
    ----------------
    {
        "success": true,
        "data": {
            "sequence_identity": 85.2,
            "human_gc_content": 52.3,
            "animal_gc_content": 48.7,
            "health_risk": {
                "predicted_mutation_rate": 0.008,
                "risk_level": "Low",
                "gas_level": 15.5
            },
            "comparison_summary": {
                "gc_difference": 3.6,
                "identity_category": "High (Same Genus)"
            }
        },
        "error": null
    }
    """
    try:
        # Parse JSON request data
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided',
                'data': None
            }), 400

        # Extract and validate input parameters
        human_seq = data.get('human_sequence', '').strip()
        animal_seq = data.get('animal_sequence', '').strip()
        gas_level = data.get('gas_level', 0.0)

        # Validate DNA sequences
        if not validate_dna_sequence(human_seq):
            return jsonify({
                'success': False,
                'error': 'Invalid human DNA sequence. Must contain only A, T, G, C nucleotides.',
                'data': None
            }), 400

        if not validate_dna_sequence(animal_seq):
            return jsonify({
                'success': False,
                'error': 'Invalid animal DNA sequence. Must contain only A, T, G, C nucleotides.',
                'data': None
            }), 400

        # Validate gas level
        try:
            gas_level = float(gas_level)
            if gas_level < 0:
                raise ValueError("Gas level cannot be negative")
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Invalid gas level. Must be a non-negative number.',
                'data': None
            }), 400

        # Perform genomic analysis
        analysis_result = genomics_engine.analyze_sequences(human_seq, animal_seq, gas_level)

        # Return successful response
        return jsonify({
            'success': True,
            'data': analysis_result,
            'error': None
        })

    except Exception as e:
        # Handle unexpected errors
        app.logger.error(f'Analysis error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Internal server error during analysis',
            'data': None
        }), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    Serve static files (CSS, JavaScript, images).

    This endpoint handles requests for static assets used by the frontend.
    """
    return send_from_directory(app.static_folder, filename)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with JSON response for API calls."""
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Endpoint not found', 'data': None}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with JSON response for API calls."""
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Internal server error', 'data': None}), 500
    return render_template('500.html'), 500

if __name__ == '__main__':
    """
    Development server entry point.

    Runs the Flask application in debug mode for local development.
    In production, use a WSGI server like Gunicorn.
    """
    # Ensure static directory exists
    os.makedirs('static', exist_ok=True)

    # Run development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )