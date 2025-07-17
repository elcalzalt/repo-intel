from flask import Flask, render_template, request, redirect, url_for, session, flash
from home import *
from user_manager import UserManager

app = Flask(__name__)
app.secret_key = 'super-secret-key'

user_manager = UserManager()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if user_manager.authenticate_user(username, password):
            session['user_id'] = user_manager.current_user_id
            session['username'] = user_manager.current_username
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        success = user_manager.create_user(username, email, password)

        if success:
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists. Try again.', 'error')

    return render_template('register.html')

@app.route('/')
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_manager.current_user_id = session['user_id']
    user_manager.current_username = session['username']

    repos = getTrendy()
    return render_template('home.html', repos=repos)

@app.route('/search')
def search_route():
    query = request.args.get("q", "")
    results = search(query) if query else []
    return render_template('search.html', results=results, query=query)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    user_manager.logout()
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)