from flask import Flask, jsonify
from datetime import datetime, timedelta, timezone
import random

app = Flask(__name__)

@app.after_request
def cors(r):
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r

def odds():
    return {"1": round(random.uniform(1.8,3.5),2), "X": round(random.uniform(2.9,3.6),2), "2": round(random.uniform(2.5,4.2),2)}

@app.route('/')
def home():
    return jsonify({"status": "FOOTYPRO LIVE", "time": datetime.now().isoformat()})

@app.route('/api/matches')
def matches():
    now_eat = datetime.now(timezone.utc) + timedelta(hours=3)
    games = []
    teams = [("Gor Mahia","AFC Leopards"),("Tusker","KCB"),("Bandari","Ulinzi Stars"),("Shabana","Homeboyz")]

    for i, (h,a) in enumerate(teams):
        day = 0 if i < 2 else 1
        d = now_eat + timedelta(days=day)
        # Time ya baadaye tu, si ya asubuhi kama ni usiku
        if day == 0:
            hr = now_eat.hour + 1 + i
            if hr > 22: 
                hr = 15
                day = 1
                d = now_eat + timedelta(days=1)
        else:
            hr = 15 + i

        dt = d.replace(hour=hr, minute=0, second=0, microsecond=0)
        if dt.timestamp() < now_eat.timestamp() - 3600:
            continue

        games.append({
            "home": h, "away": a,
            "time": dt.strftime("%H:%M"),
            "date": dt.strftime("%Y-%m-%d"),
            "day_diff": day,
            "league_name": "FKF PREMIER LEAGUE",
            "timestamp": int(dt.timestamp()),
            "odds": odds()
        })
    
    games.sort(key=lambda x: x['timestamp'])
    return jsonify(games)

if __name__ == '__main__':
    app.run()
