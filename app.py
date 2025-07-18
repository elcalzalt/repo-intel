from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from home import *
from user_manager import UserManager
from cache_db import CacheDatabase

app = Flask(__name__)
app.secret_key = 'super-secret-key'

cache = CacheDatabase()
user_manager = UserManager(cache)

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
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get("q", "")
    results = search(query) if query else []
    return render_template('search.html', results=results, query=query)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('profile.html')

@app.route('/logout')
def logout():
    user_manager.logout()
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/repo/<path:repo_name>', methods=['GET', 'POST'])
def repo_analysis(repo_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Use full repo info from form
    full_name = request.form.get('full_name', repo_name)
    owner = request.form.get('owner', full_name.split('/', 1)[0])
    name = request.form.get('name', full_name.split('/', 1)[1] if '/' in full_name else full_name)
    description = request.form.get('description', '')
    url = request.form.get('url', '')
    stars = request.form.get('stars', '')
    forks = request.form.get('forks', '')
    updated_at = request.form.get('updated_at', '')

    # Build repo_data
    repo_data = {
        'name': name,
        'owner': owner,
        'full_name': full_name,
        'description': description,
        'url': url,
        'stars': stars,
        'forks': forks,
        'updated_at': updated_at
    }
    
    return render_template('repo_analysis.html', repo=repo_data)

# API Routes for repository analysis
@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = request.get_json()
    repo_name = data.get('repo_name')
    
    # Mock summary - replace with actual AI analysis
    summary = user_manager.summarize_repo(repo_name)
    
    return jsonify({
        'success': True,
        'summary': summary
    })

@app.route('/api/file-tree', methods=['POST'])
def api_file_tree():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = request.get_json()
    repo_name = data.get('repo_name')
    # default to root if no path provided
    file_path = data.get('file_path', '')
    # fetch directory listing
    file_tree = user_manager.get_file_tree(repo_name, file_path)
    return jsonify({
        'success': True,
        'file_tree': file_tree
    })

@app.route('/api/scan', methods=['POST'])
def api_scan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = request.get_json()
    repo_name = data.get('repo_name')
    file_path = data.get('file_path')
    
    # Mock scan results - replace with actual security scanning
    scan_results = user_manager.scan_file(repo_name, file_path)
    
    return jsonify({
        'success': True,
        'scan_results': scan_results
    })

@app.route('/api/bookmark', methods=['POST'])
def api_bookmark():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = request.get_json()
    repo_url = data.get('repo_url')
    repo_name = data.get('repo_name')
    repo_owner = data.get('repo_owner')
    
    # Mock bookmark save - replace with actual database storage
    # In real implementation, save to user's bookmarks in database
    
    return jsonify({
        'success': True,
        'message': f'Repository {repo_name} has been bookmarked successfully'
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)