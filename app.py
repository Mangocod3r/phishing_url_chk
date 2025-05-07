#importing required libraries

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import json
import os
from dotenv import load_dotenv
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

# Load environment variables
load_dotenv()

# Load model from environment variable or default path
MODEL_PATH = os.getenv('MODEL_PATH', 'pickle/model.pkl')
with open(MODEL_PATH, "rb") as file:
    gbc = pickle.load(file)

app = Flask(__name__)
# Configure CORS to allow all origins
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 

        y_pred = gbc.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('index.html', xx=round(y_pro_non_phishing,2), url=url)
    return render_template("index.html", xx=-1)

@app.route("/api/check_url", methods=["POST", "OPTIONS"])
def check_url():
    if request.method == "OPTIONS":
        return "", 200
        
    data = request.get_json()
    print(data)
    url = data.get("url")
    
    if url:
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)

        # Prediction
        y_pred = gbc.predict(x)[0]
        is_safe = bool(y_pred == 1)  # Convert numpy.bool_ to Python bool
        y_pro_phishing = float(gbc.predict_proba(x)[0, 0])  # Convert to Python float
        y_pro_non_phishing = float(gbc.predict_proba(x)[0, 1])  # Convert to Python float
        
        # Create a response
        response = {
            "url": url,
            "safe": is_safe,
            "confidence": round(y_pro_non_phishing * 100, 2) if is_safe else round(y_pro_phishing * 100, 2),
            "unsafe_confidence": round(y_pro_phishing * 100, 2) if is_safe else round(y_pro_non_phishing * 100, 2)
        }
        return jsonify(response)
    
    return jsonify({"error": "No URL provided"}), 400

@app.route("/api/cache_stats", methods=["GET"])
def cache_stats():
    try:
        with open('cache_stats.json', 'r') as f:
            stats = json.load(f)
            
        # Add some business metrics
        if stats["requests_served"] > 0:
            # Estimate API cost savings (assuming $0.002 per request)
            cost_per_request = 0.002
            money_saved = (stats["cache_hits"] * cost_per_request)
            
            # Estimate bandwidth saved (assuming 1KB per request)
            kb_per_request = 1
            bandwidth_saved = (stats["cache_hits"] * kb_per_request)
            
            stats.update({
                "estimated_cost_savings": f"${money_saved:.2f}",
                "bandwidth_saved_kb": bandwidth_saved,
                "performance_improvement": f"{stats['avg_time_saved']*1000:.0f}ms per request"
            })
            
        return jsonify(stats)
    except FileNotFoundError:
        return jsonify({"error": "No cache statistics available yet"}), 404

if __name__ == "__main__":
    # Get configuration from environment variables
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5001))
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    app.run(debug=DEBUG, host=HOST, port=PORT)