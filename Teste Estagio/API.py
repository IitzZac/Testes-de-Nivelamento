from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

from flask_cors import CORS
CORS(app)

CSV_PATH = "Scripts .sql/Dados_ANS/Relatorio_cadop.csv"


if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH, delimiter=";", encoding="utf-8")
else:
    df = pd.DataFrame()  

@app.route("/operadoras", methods=["GET"])
def buscar_operadoras():
    
    query = request.args.get("q", "").strip().lower()
    
    if query and not df.empty:
        resultado = df[df["razao_social"].str.lower().str.contains(query, na=False) |
                       df["cnpj"].astype(str).str.contains(query)]
        return jsonify(resultado.to_dict(orient="records"))

    return jsonify([])  

if __name__ == "__main__":
    app.run(debug=True)
