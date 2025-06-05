from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("maladies_symptomes_reels.csv", encoding="utf-8-sig")

def rechercher_diagnostics(symptomes_utilisateur, df, top_n=7):
    symptomes_utilisateur = [s.strip().lower() for s in symptomes_utilisateur.split(",") if s.strip()]
    scores = {}

    for _, row in df.iterrows():
        maladie = row["Maladie"]
        symptomes_maladie = [s.strip() for s in row["Symptômes"].split(",")]
        nb_total_symptomes = len(symptomes_maladie)
        match_count = sum(1 for s in symptomes_utilisateur for sm in symptomes_maladie if s in sm)

        if match_count > 0:
            pourcentage = (match_count / nb_total_symptomes) * 100
            scores[maladie] = (match_count, pourcentage)

    resultats = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)
    return resultats[:top_n]

@app.route("/diagnostic", methods=["POST"])
def diagnostic():
    data = request.get_json()
    symptomes = data.get("symptomes", "")
    resultats = rechercher_diagnostics(symptomes, df)
    reponse = [
        {"maladie": maladie, "correspondance": nb, "pourcentage": round(pct)}
        for maladie, (nb, pct) in resultats
    ]
    return jsonify(reponse)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)