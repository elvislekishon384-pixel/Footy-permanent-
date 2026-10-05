import os
from flask import Flask
app=Flask(__name__)
@app.route('/')
def home():
    return open('index.html').read() if os.path.exists('index.html') else 'UPLOAD index.html'
if __name__=='__main__':
    port=int(os.environ.get("PORT",10000))
    app.run(host='0.0.0.0',port=port)
