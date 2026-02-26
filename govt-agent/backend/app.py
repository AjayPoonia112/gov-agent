import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Ensure you have templates/index.html in your repo
    return render_template('index.html')

@app.route('/healthz')
def healthz():
    return {'status': 'ok'}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
