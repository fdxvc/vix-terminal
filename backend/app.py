from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
from datetime import datetime
import pytz

app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin

def get_vix_data():
    try:
        # Récupération du VIX Spot
        vix_spot = yf.Ticker("^VIX")
        spot = vix_spot.history(period="1d")["Close"].iloc[-1]

        # Récupération des 6 prochains contrats futures VX (M1 à M6)
        futures = []
        for i in range(1, 7):
            ticker = f"VX{i}=F"
            contract = yf.Ticker(ticker)
            price = contract.history(period="1d")["Close"].iloc[-1]
            futures.append(price)

        # Timestamp et statut
        timestamp = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        status = "delayed 15m"

        return {
            "spot": round(float(spot), 2),
            "futures": [round(float(f), 2) for f in futures],
            "timestamp": timestamp,
            "status": status
        }
    except Exception as e:
        # Valeurs de repli en cas d'erreur
        return {
            "spot": 20.0,
            "futures": [20.5, 21.0, 21.5, 22.0, 22.5, 23.0],
            "timestamp": datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "status": f"fallback (error: {str(e)})"
        }

@app.route('/api/vix-data', methods=['GET'])
def vix_data():
    data = get_vix_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)