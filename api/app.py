from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import hf_hub_download
import joblib, sys, os

BASE = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE, "model")
sys.path.append(MODEL_DIR)

from features import extract_features

app = Flask(__name__)
CORS(app)

MODEL_PATH = hf_hub_download(
    repo_id="hex-sentinel/phishing-detector-model",
    filename="phishing_model.pkl"
)

model = joblib.load(MODEL_PATH)


# ── Routes ───────────────────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({'error': 'Missing "url" in request body'}), 400

    url = data['url'].strip()
    if not url:
        return jsonify({'error': 'URL cannot be empty'}), 400

    try:
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
    return jsonify({'status': 'ok', 'model': 'loaded'})

# ── Run ──────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)