from flask import Flask, render_template_string, redirect, session
import random
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "footy-pro-2026-secret"

MOCK_MATCHES = [
    {"home": "Lens", "away": "Sporting", "time": "20:45", "league": "Champions League", "odd_home": 2.1, "odd_draw": 3.4, "odd_away": 3.2, "tip": "Over 1.5", "conf": "87%"},
    {"home": "Arsenal", "away": "Lille", "time": "20:45", "league": "Champions League", "odd_home": 1.65, "odd_draw": 3.8, "odd_away": 4.5, "tip": "Arsenal Win", "conf": "82%"},
    {"home": "Atletico Madrid", "away": "Man United", "time": "21:00", "league": "Champions League", "odd_home": 2.3, "odd_draw": 3.3, "odd_away": 2.9, "tip": "BTTS Yes", "conf": "79%"},
    {"home": "Gor Mahia", "away": "AFC Leopards", "time": "15:00", "league": "FKF PL", "odd_home": 2.0, "odd_draw": 3.0, "odd_away": 3.5, "tip": "Under 2.5", "conf": "75%"},
]

HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>FOOTY PRO 2026</title>
<style>body{margin:0;font-family:Arial;background:#0f172a;color:white}.header{background:#1e293b;padding:15px;display:flex;justify-content:space-between;align-items:center}.logo{font-weight:bold;font-size:20px;color:#22c55e}.btn{background:#22c55e;color:black;border:none;padding:10px 18px;border-radius:8px;font-weight:bold;cursor:pointer}.card{background:#1e293b;margin:12px;border-radius:12px;padding:15px;border:1px solid #334155}.odd{display:inline-block;background:#0f172a;padding:6px 10px;border-radius:6px;margin:3px;font-size:13px}.tip{background:#22c55e;color:black;padding:4px 8px;border-radius:5px;font-weight:bold;font-size:12px}.top{color:#94a3b8;font-size:12px}.paid{background:#16a34a;padding:12px;border-radius:8px;text-align:center;margin:10px 12px;font-weight:bold}</style>
</head><body>
<div class="header"><div class="logo">⚽ FOOTY PRO 2026</div><div>{% if session.get('paid') %}<span style="color:#22c55e">Umeshalipa!</span> <a href="/logout" style="color:white;margin-left:10px">Logout</a>{% else %}<a href="/pay"><button class="btn">Lipa 50 KES</button></a>{% endif %}</div></div>
<div style="padding:12px"><button class="btn" style="width:100%;padding:14px" onclick="location.href='/fetch'">🔄 Fetch Mechi</button></div>
{% if session.get('paid') %}<div class="paid">✅ Umeshalipa - Karibu! Odds Zote Ziko Hapa</div>{% endif %}
{% for m in matches %}<div class="card"><div class="top">{{m.league}} • {{m.time}} • {{m.conf}}</div><div style="font-size:18px;margin:8px 0;font-weight:bold">{{m.home}} vs {{m.away}}</div><div><span class="odd">1: {{m.odd_home}}</span><span class="odd">X: {{m.odd_draw}}</span><span class="odd">2: {{m.odd_away}}</span><span class="tip">{{m.tip}}</span></div></div>{% endfor %}</body></html>
"""
@app.route('/')
def home(): return render_template_string(HTML, matches=MOCK_MATCHES, now=datetime.now().strftime("%H:%M"))
@app.route('/fetch')
def fetch(): random.shuffle(MOCK_MATCHES); return redirect('/')
@app.route('/pay')
def pay(): session['paid']=True; return redirect('/')
@app.route('/logout')
def logout(): session.clear(); return redirect('/')
if __name__ == '__main__': app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
