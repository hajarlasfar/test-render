# -*- coding: utf-8 -*-
"""
app.py — Mini-application de test pour Render
=============================================
Une page web avec un petit formulaire : on tape son prénom, la page répond.
Sert uniquement à vérifier que la mise en ligne sur Render fonctionne.

Sur ton PC :   python app.py   puis ouvrir http://127.0.0.1:5000
Sur Render :   Start Command = python app.py
"""

import os
from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, request
from waitress import serve

app = Flask(__name__)

PAGE = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Test Render</title>
<style>
 body{{font-family:Segoe UI,Arial,sans-serif;background:#f3f6fb;margin:0;display:flex;
      min-height:100vh;align-items:center;justify-content:center}}
 .carte{{background:#fff;padding:36px 40px;border-radius:16px;box-shadow:0 8px 30px rgba(0,0,0,.08);
        max-width:420px;width:90%;text-align:center}}
 h1{{margin:0 0 6px;color:#1e3a5f;font-size:24px}}
 p{{color:#555}}
 input{{padding:10px 12px;border:1px solid #ccd5e0;border-radius:8px;font-size:15px;width:60%}}
 button{{padding:10px 18px;border:none;border-radius:8px;background:#1e3a5f;color:#fff;
        font-size:15px;cursor:pointer;margin-left:6px}}
 .reponse{{margin-top:20px;padding:12px;border-radius:8px;background:#e8f5ee;color:#1d6b43;font-weight:600}}
 small{{color:#999}}
</style></head>
<body><div class="carte">
 <h1>✅ Mon application est en ligne !</h1>
 <p>Heure du serveur : <b>{heure}</b></p>
 <form method="post">
  <input name="prenom" placeholder="Ton prénom" required>
  <button type="submit">Envoyer</button>
 </form>
 {reponse}
 <p><small>Test de mise en ligne avec Render</small></p>
</div></body></html>"""


@app.route("/", methods=["GET", "POST"])
def accueil():
    heure = datetime.now(ZoneInfo("Africa/Casablanca")).strftime("%d/%m/%Y %H:%M:%S")
    reponse = ""
    if request.method == "POST":
        prenom = (request.form.get("prenom") or "").strip()[:40]
        # on échappe le texte saisi pour la sécurité
        prenom = prenom.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        reponse = f'<div class="reponse">Bonjour {prenom} 👋 Le serveur a bien reçu ton message.</div>'
    return PAGE.format(heure=heure, reponse=reponse)


@app.get("/sante")
def sante():
    return "ok"


if __name__ == "__main__":
    # Render donne le port dans la variable PORT ; sur ton PC on utilise 5000
    port = int(os.environ.get("PORT", 5000))
    print(f"Application démarrée sur le port {port}")
    serve(app, host="0.0.0.0", port=port)
