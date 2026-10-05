from flask import Flask, send_from_directory
import os
from datetime import datetime, timedelta
import json, random

app = Flask(__name__)

# FAKE BUT REALISTIC MATCHES GENERATOR - Leo hadi Next Week
def get_matches():
    leagues = [
        {"name": "FKF PREMIER LEAGUE", "flag": "🇰🇪"},
        {"name": "PREMIER LEAGUE", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
        {"name": "LA LIGA", "flag": "🇪🇸"},
        {"name": "SERIE A", "flag": "🇮🇹"},
        {"name": "BUNDESLIGA", "flag": "🇩🇪"},
        {"name": "LIGUE 1", "flag": "🇫🇷"},
        {"name": "CHAMPIONS LEAGUE", "flag": "🏆"},
    ]
    teams = {
        "🇰🇪": [("Gor Mahia","AFC Leopards"),("Tusker","KCB"),("Bandari","Ulinzi Stars"),("Kakamega Homeboyz","Nairobi City Stars")],
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿": [("Man City","Arsenal"),("Liverpool","Chelsea"),("Man United","Tottenham"),("Newcastle","Brighton"),("West Ham","Aston Villa")],
        "🇪🇸": [("Real Madrid","Barcelona"),("Atletico Madrid","Sevilla"),("Villarreal","Real Sociedad")],
        "🇮🇹": [("Inter","AC Milan"),("Juventus","Napoli"),("Roma","Lazio")],
        "🇩🇪": [("Bayern Munich","Dortmund"),("Leverkusen","Leipzig")],
        "🇫🇷": [("PSG","Marseille"),("Lyon","Monaco")],
        "🏆": [("Real Madrid","Man City"),("Arsenal","Bayern"),("PSG","Barcelona")]
    }
    matches=[]
    now=datetime.now()
    for i in range(45): # 45 matches
        league = random.choice(leagues)
        t1,t2 = random.choice(teams[league["flag"]])
        # Date: today, tomorrow, next 7 days
        day_offset = random.choice([0,0,0,1,1,2,3,5,7]) # more today
        date = now + timedelta(days=day_offset, hours=random.randint(0,23))
        is_live = random.random() < 0.25 and day_offset==0 # 25% live if today
        
        matches.append({
            "id": i,
            "league": league["name"],
            "flag": league["flag"],
            "home": t1,
            "away": t2,
            "time": date.strftime("%H:%M"),
            "date_label": "LIVE" if is_live else "Today" if day_offset==0 else "Tomorrow" if day_offset==1 else (now+timedelta(days=day_offset)).strftime("%a %d %b"),
            "day": day_offset,
            "live": is_live,
            "score": f"{random.randint(0,2)}-{random.randint(0,2)}" if is_live else None,
            "minute": random.randint(10,88) if is_live else None,
            "odds": [round(random.uniform(1.6,4.5),2), round(random.uniform(2.8,4.2),2), round(random.uniform(1.8,5.0),2)]
        })
    return sorted(matches, key=lambda x: (x["day"], x["time"]))

@app.route('/api/matches')
def api_matches():
    return json.dumps(get_matches())

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(path):
        return send_from_directory('.', path)
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
