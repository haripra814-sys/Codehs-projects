from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def analyze_dna(dna_sequence: str, toxin_level: float) -> dict:
    """
    Estimate oxidative DNA damage (8-oxoG) based on toxin level and sequence.
    The model is intentionally simplified for education and public outreach.
    """
    seq = "".join(dna_sequence.upper().split())
    valid_bases = {"A", "T", "C", "G"}

    if not seq:
        raise ValueError("DNA sequence cannot be empty.")
    if any(base not in valid_bases for base in seq):
        raise ValueError("DNA sequence contains invalid characters.")
    if toxin_level < 0 or toxin_level > 100:
        raise ValueError("Toxin level must be between 0 and 100.")

    g_count = seq.count("G")
    sequence_length = len(seq)

    # Simple educational estimate:
    # baseline random oxidative damage + guanine susceptibility factor.
    baseline_damage = (toxin_level / 100.0) * (sequence_length * 0.01)
    guanine_damage = (toxin_level / 100.0) * (g_count * 0.08)
    oxo8g_mutations = int(round(baseline_damage + guanine_damage))

    dna_integrity = max(0, 100 - int(round((oxo8g_mutations / max(1, sequence_length)) * 1000)))
    community_health_score = max(0, min(100, int(round(90 - (toxin_level * 0.6) - (oxo8g_mutations * 0.2)))))

    return {
        "sequence_length": sequence_length,
        "guanine_count": g_count,
        "toxin_level": toxin_level,
        "oxo8g_mutations": oxo8g_mutations,
        "dna_integrity": dna_integrity,
        "community_health_score": community_health_score,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    dna_sequence = payload.get("dna_sequence", "")
    toxin_level = float(payload.get("toxin_level", 0))

    try:
        result = analyze_dna(dna_sequence, toxin_level)
        return jsonify({"ok": True, "result": result})
    except (ValueError, TypeError) as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


if __name__ == "__main__":
    app.run(debug=True)
