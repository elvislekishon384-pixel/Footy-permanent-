from flask import Flask, send_from_directory
import os
from datetime import datetime, timedelta
import json, random

app = Flask(__name__)

def get_matches():
    leagues = [
        {"name": "FKF PREMIER LEAGUE", "flag": "🇰🇪"},
        {"name": "PREMIER LEAGUE", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
        {"name": "LA LIGA", "flag": "🇪🇸"},
        {"name": "SERIE A", "flag": "🇮🇹"},
        {"name": "BUNDESLIGA", "flag": "🇩🇪"},
        {"name": "CHAMPIONS LEAGUE", "flag": "🏆"},
    ]
    teams = {
        "🇰🇪": [("Gor Mahia","AFC Leopards"),("Tusker","KCB"),("Bandari","Ulinzi"),("Kakamega Homeboyz","City Stars"),("Sofapaka","Police FC")],
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿": [("Man City","Arsenal"),("Liverpool","Chelsea"),("Man United","Tottenham"),("Newcastle","Brighton"),("West Ham","Aston Villa"),("Everton","Fulham")],
        "🇪🇸": [("Real Madrid","Barcelona"),("Atletico Madrid","Sevilla"),("Villarreal","Real Sociedad"),("Athletic Bilbao","Valencia")],
        "🇮🇹": [("Inter","AC Milan"),("Juventus","Napoli"),("Roma","Lazio"),("Atalanta","Fiorentina")],
        "🇩🇪": [("Bayern Munich","Dortmund"),("Leverkusen","Leipzig"),("Stuttgart","Frankfurt")],
        "🏆": [("Real Madrid","Man City"),("Arsenal","Bayern"),("PSG","Barcelona"),("Inter","Atletico")]
    }
    # TIME HALISI ZA MPIRA - 13:00, 15:00, 17:30, 19:45, 21:00, 22:00
    real_times = ["13:00","14:00","15:00","15:30","16:00","17:00","17:30","18:00","19:00","19:45","20:00","21:00","22:00"]

    matches=[]
    now = datetime.now()
    today_str = now.strftime("%d %b %Y")

    for i in range(50):
        league = random.choice(leagues)
        t1,t2 = random.choice(teams[league["flag"]])
        day_offset = random.choices([0,0,0,0,1,2,3,5,7], weights=[25,25,20,15,10,5,5,3,2])[0]
        date_obj = now + timedelta(days=day_offset)

        # Time logic
        if day_offset == 0:
            # Leo - time from now onwards
            time_str = random.choice(real_times)
            # Hakikisha si usiku sana kama ni 9pm
            if now.hour > 18:
                time_str = random.choice(["19:45","20:00","21:00","22:00"])
        else:
            time_str = random.choice(real_times)

        is_live = False
        if day_offset == 0 and random.random() < 0.35:
            is_live = True
            time_str = f"{random.randint(10,85)}'" # minute

        # Date label proper
        if is_live:
            date_label = "LIVE"
        elif day_offset == 0:
            date_label = f"Today, {today_str}"
        elif day_offset == 1:
            date_label = f"Tomorrow, {(now+timedelta(days=1)).strftime('%d %b')}"
        else:
            date_label = date_obj.strftime("%a %d %b %Y")

        matches.append({
            "id": i,
            "league": league["name"],
            "flag": league["flag"],
            "home": t1,
            "away": t2,
            "time": time_str,
            "date_label": date_label,
            "full_date": date_obj.strftime("%Y-%m-%d"),
            "day": day_offset,
            "live": is_live,
            "score": f"{random.randint(0,3)}-{random.randint(0,3)}" if is_live else None,
            "minute": random.randint(12,89) if is_live else None,
            "odds": [round(random.uniform(1.55,4.8),2), round(random.uniform(2.9,4.1),2), round(random.uniform(1.9,5.2),2)]
        })
    return sorted(matches, key=lambda x: (x["day"], x["time"]))

@app.route('/api/matches')
def api_matches():
    # Add server time pia
    now = datetime.now()
    return json.dumps({
        "server_time": now.strftime("%A, %d %B %Y - %H:%M:%S"),
        "matches": get_matches()
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path!= "" and os.path.exists(path):
        return send_from_directory('.', path)
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
