from flask import Flask, render_template
from home import getTrendy

app = Flask(__name__)

@app.route('/')
def home():
    repos = getTrendy()
    return render_template('home.html', repos=repos)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")