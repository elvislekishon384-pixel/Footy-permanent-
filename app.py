from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import pytz
import random

app = Flask(__name__)
CORS(app)

EAT = pytz.timezone('Africa/Nairobi')

# Leagues tunazotaka - ESPN codes
LEAGUES = {
    "FKF PREMIER LEAGUE": "ken.1",
    "PREMIER LEAGUE": "eng.1",
    "LA LIGA": "esp.1",
    "SERIE A": "ita.1"
}

def generate_odds():
    home = round(random.uniform(1.8, 3.5), 2)
    draw = round(random.uniform(2.9, 3.6), 2)
    away = round(random.uniform(2.5, 4.2), 2)
    return {"1": home, "X": draw, "2": away}

def fetch_espn(league_code, date_str):
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_code}/scoreboard?dates={date_str}"
        r = requests.get(url, timeout=8).json()
        games = []
        for ev in r.get('events', []):
            comp = ev['competitions'][0]
            home = comp['competitors'][0] if comp['competitors'][0]['homeAway']=='home' else comp['competitors'][1]
            away = comp['competitors'][1] if comp['competitors'][0]['homeAway']=='home' else comp['competitors'][0]
            dt = datetime.fromisoformat(ev['date'].replace('Z','+00:00')).astimezone(EAT)
            games.append({
                "home": home['team']['displayName'],
                "away": away['team']['displayName'],
                "time": dt.strftime("%H:%M"),
                "date": dt.strftime("%Y-%m-%d"),
                "date_label": dt.strftime("%d %b %Y"),
                "timestamp": int(dt.timestamp()),
                "league": league_code,
                "odds": generate_odds()
            })
        return games
    except:
        return []

@app.route('/api/matches')
def matches():
    now = datetime.now(EAT)
    today_str = now.strftime("%Y%m%d")
    tomorrow_str = (now + timedelta(days=1)).strftime("%Y%m%d")

    all_games = []

    # Leo + Kesho + Next 7 days
    for i in range(7):
        d = now + timedelta(days=i)
        d_str = d.strftime("%Y%m%d")
        for league_name, code in LEAGUES.items():
            data = fetch_espn(code, d_str)
            for g in data:
                g['league_name'] = league_name
                g['day_diff'] = i # 0=leo, 1=kesho
                all_games.append(g)

    # Kama ESPN haina FKF leo, weka za leo na random time ya baadae (usiweke saa 9 ya asubuhi kama ni jioni)
    if not any(x['league_name']=='FKF PREMIER LEAGUE' for x in all_games):
        # generate realistic today games with future time only
        fkf_teams = [("Gor Mahia","AFC Leopards"),("Tusker","KCB"),("Bandari","Ulinzi Stars"),("Shabana","Kakamega Homeboyz")]
        for h,a in fkf_teams:
            future_hour = random.randint(now.hour+1, 20) if now.hour < 20 else 15
            future_hour = min(future_hour, 20)
            dt = now.replace(hour=future_hour, minute=0)
            all_games.append({
                "home": h, "away": a,
                "time": dt.strftime("%H:%M"),
                "date": dt.strftime("%Y-%m-%d"),
                "date_label": f"Today, {dt.strftime('%d %b %Y')}",
                "timestamp": int(dt.timestamp()),
                "league": "ken.1",
                "league_name": "FKF PREMIER LEAGUE",
                "day_diff": 0,
                "odds": generate_odds()
            })

    # PANGA KWA MUDA - game za zamani zisifichwe
    all_games = [g for g in all_games if g['timestamp'] >= int((now - timedelta(hours=2)).timestamp())]
    all_games.sort(key=lambda x: x['timestamp'])

    return jsonify(all_games)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
