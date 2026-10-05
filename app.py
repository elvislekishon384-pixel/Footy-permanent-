from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FOOTY PRO 2026</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:system-ui}
body{background:#0f1923;color:#fff;padding-bottom:80px}
.top{background:#ffcc00;padding:10px;display:flex;justify-content:space-between;align-items:center}
.logo{font-weight:900;color:#000;font-size:14px}
.bal{background:#000;color:#ffcc00;padding:6px 12px;border-radius:20px;font-size:11px;font-weight:800}
.nav2{background:#1a2935;display:flex;gap:6px;padding:8px;overflow-x:auto}
.n2{padding:7px 14px;border-radius:20px;background:#253a4a;color:#aaa;font-size:12px;border:none;font-weight:700}
.n2.active{background:#fff;color:#000}
.sub{display:flex;gap:6px;padding:8px}
.s{padding:6px 14px;background:#1c2f3e;border-radius:6px;font-size:12px;color:#8aa1b5;border:none}
.s.active{background:#00e676;color:#000}
.match{background:#1a2935;margin:8px;border-radius:10px;overflow:hidden}
.m-top{display:flex;justify-content:space-between;padding:6px 10px;font-size:10px;color:#8aa1b5;background:#16202b}
.teams{padding:10px;font-weight:700;font-size:13px}
.odds{display:flex;gap:5px;padding:0 8px 8px}
.od{flex:1;background:#253a4a;border-radius:6px;padding:10px;text-align:center;font-weight:800;font-size:12px}
.page{display:none}.page.active{display:block}
.modal{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.85);display:none;z-index:50;align-items:center;justify-content:center;padding:15px}
.modal.show{display:flex}
.card{background:#1a2935;width:100%;max-width:360px;border-radius:12px;padding:18px}
.card input{width:100%;padding:11px;background:#0f1923;border:1px solid #333;border-radius:8px;color:#fff;margin:6px 0}
.avi-bg{background:#0a121a;height:220px;position:relative;border-radius:10px;margin:10px;overflow:hidden}
.mult{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:42px;font-weight:900;color:#ffcc00}
.plane{position:absolute;font-size:28px;bottom:40px;left:20px}
.controls{display:flex;gap:8px;margin:10px}
.cbox{flex:1;background:#1a2935;padding:10px;border-radius:10px;text-align:center}
.h{display:flex;gap:5px;padding:8px;overflow-x:auto}
.hi{padding:3px 7px;border-radius:10px;font-size:10px;font-weight:800}
.low{background:#ff3b30}.mid{background:#ffcc00;color:#000}.high{background:#00e676;color:#000}
.slip{position:fixed;bottom:0;left:0;right:0;background:#ffcc00;padding:10px 14px;display:flex;justify-content:space-between;color:#000;font-weight:900}
</style></head><body>
<div class="top"><div class="logo">⚽ FOOTY PRO 2026</div><div style="display:flex;gap:6px;align-items:center"><div class="bal" id="bal">KES 0.00</div><button id="lb" onclick="openM('login')" style="border:none;border-radius:20px;padding:6px 12px;background:#000;color:#fff;font-weight:800;font-size:11px">Login</button><button id="rb" onclick="openM('reg')" style="border:none;border-radius:20px;padding:6px 12px;background:#000;color:#fff;font-weight:800;font-size:11px">Join</button><button id="ub" style="display:none;border:none;border-radius:20px;padding:6px 12px;background:#000;color:#ffcc00;font-weight:800" onclick="logout()"></button></div></div>
<div class="nav2"><button class="n2 active" onclick="showP('soccer',this)">⚽ Soccer</button><button class="n2" onclick="showP('aviator',this)">✈️ Aviator</button><button class="n2" onclick="showP('account',this)">👤 Account</button></div>
<div id="soccer" class="page active"><div class="sub"><button class="s active" onclick="filterD('today',this)">Today</button><button class="s" onclick="filterD('tomorrow',this)">Tomorrow</button><button class="s" onclick="filterD('live',this)">Live</button></div><div id="matches"></div></div>
<div id="aviator" class="page"><div class="h" id="hist"></div><div class="avi-bg"><div class="mult" id="mult">1.00x</div><div class="plane" id="plane">✈️</div></div><div class="controls"><div class="cbox"><input id="bet1" value="20" style="width:100%;padding:8px;background:#0f1923;border:1px solid #333;color:#fff;border-radius:6px;text-align:center"><button id="b1" onclick="placeB(1)" style="width:100%;margin-top:6px;padding:10px;background:#00e676;border:none;border-radius:6px;font-weight:900">BET</button></div><div class="cbox"><input id="bet2" value="50" style="width:100%;padding:8px;background:#0f1923;border:1px solid #333;color:#fff;border-radius:6px;text-align:center"><button id="b2" onclick="placeB(2)" style="width:100%;margin-top:6px;padding:10px;background:#00e676;border:none;border-radius:6px;font-weight:900">BET</button></div></div></div>
<div id="account" class="page"><div style="padding:15px"><div id="accInfo" style="background:#1a2935;padding:14px;border-radius:10px"></div><button onclick="window.open('https://wa.me/254700000000?text=Hi','_blank')" style="width:100%;margin-top:10px;padding:12px;background:#25D366;border:none;border-radius:8px;color:#fff;font-weight:900">💬 WhatsApp</button></div></div>
<div class="slip" id="slip" style="display:none"><span id="sc">0 Bets</span><span id="so">Odds 1.00</span></div>
<div class="modal" id="loginM"><div class="card"><h3 style="color:#ffcc00">Login</h3><input id="lPh" placeholder="Phone"><input id="lPw" type="password" placeholder="Password"><button onclick="doLogin()" style="width:100%;padding:11px;background:#ffcc00;border:none;border-radius:8px;font-weight:900;margin-top:8px">Login</button><button onclick="closeM()" style="width:100%;padding:10px;background:#253a4a;color:#fff;border:none;border-radius:8px;margin-top:6px">Cancel</button></div></div>
<div class="modal" id="regM"><div class="card"><h3 style="color:#ffcc00">Join - Bonus 50</h3><input id="rNa" placeholder="Name"><input id="rPh" placeholder="Phone 07xx"><input id="rPw" type="password" placeholder="Password"><button onclick="doReg()" style="width:100%;padding:11px;background:#ffcc00;border:none;border-radius:8px;font-weight:900;margin-top:8px">Create</button><button onclick="closeM()" style="width:100%;padding:10px;background:#253a4a;color:#fff;border:none;border-radius:8px;margin-top:6px">Cancel</button></div></div>
<script>
let curU=JSON.parse(localStorage.getItem('fp_u')||'null'),bets=[],cur='today';
const games={today:[{lg:'FKF PL',t:'15:00',a:'Gor Mahia',b:'AFC Leopards',o:['2.1','3.0','3.4'],p:'Under 2.5'},{lg:'EPL',t:'17:30',a:'Man City',b:'Arsenal',o:['2.15','3.4','3.2'],p:'Over 1.5'},{lg:'UCL',t:'20:45',a:'Lens',b:'Sporting',o:['2.4','3.2','2.9'],p:'Over 1.5'}],tomorrow:[{lg:'FKF PL',t:'14:00',a:'Tusker',b:'KCB',o:['1.9','3.1','4.0'],p:'Home Win'}],live:[{lg:'FKF PL 67',t:'LIVE',a:'Ulinzi',b:'Sharks',o:['1.85','2.1','5.2'],p:'1-0'}]};
function upd(){if(curU){document.getElementById('bal').innerText='KES '+curU.bal.to
