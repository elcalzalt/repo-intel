from flask import Flask, render_template, request
from home import *

app = Flask(__name__)

@app.route('/login')
def login(): #add any needed auth logic here
    return render_template('login.html')

@app.route('/home')
def home():
    repos = getTrendy()
    return render_template('home.html', repos=repos)

@app.route('/search')
def search_route():
    query = request.args.get("q", "")
    results = search(query) if query else []
    return render_template('search.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")