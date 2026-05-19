from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import hf_hub_download
from urllib.parse import urlparse
import joblib, sys, os

# ── Path setup ───────────────────────────────
# app.py is in api/  →  features.py is in model/  →  go up one level then into model/
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'model'))
from features import extract_features

app = Flask(__name__)
CORS(app)

# ── Lazy model loader ────────────────────────
# Model is NOT loaded at startup — this prevents Railway 502s
# caused by slow/failed downloads blocking port binding.
_model = None

def get_model():
    global _model
    if _model is None:
        print("Downloading model from HuggingFace Hub...")
        model_path = hf_hub_download(
            repo_id="hex-sentinel/phishing-detector-model",
            filename="phishing_model.pkl"
        )
        _model = joblib.load(model_path)
        print("Model loaded successfully.")
    return _model


# ── Routes ───────────────────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({'error': 'Missing "url" in request body'}), 400

    url = data['url'].strip()
    if not url:
        return jsonify({'error': 'URL cannot be empty'}), 400

    # Basic URL format validation
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return jsonify({'error': 'Invalid URL format. Include scheme e.g. https://example.com'}), 400

    try:
        model   = get_model()
        features = extract_features(url)
        pred     = model.predict([features])[0]
        prob     = model.predict_proba([features])[0][1]

        return jsonify({
            'url':         url,
            'is_phishing': bool(pred),
            'confidence':  round(float(prob), 3)
        })


    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    # Reports whether the model is already loaded in memory
    return jsonify({
        'status': 'ok',
        'model':  'loaded' if _model is not None else 'not yet loaded (loads on first /predict call)'
    })


# ── Run ──────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
