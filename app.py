"""Flask application for repository analysis and user management.
Provides routes for authentication, repository operations, summarization,
file structure browsing, scanning, exporting results, and bookmarks."""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from home import *
from user_manager import UserManager
from cache_db import CacheDatabase
from time_ago import time_ago
import markdown
import subprocess, tempfile, os
from flask import send_file, make_response

app = Flask(__name__)
# Set secret key for session management
app.secret_key = 'super-secret-key'

cache = CacheDatabase()
user_manager = UserManager(cache)

@app.route('/login', methods=['GET', 'POST'])
# Route for user login; GET displays form, POST processes credentials
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
# Route for new user registration; validates and adds user to database
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
# Home page; shows trending repositories after authentication
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_manager.current_user_id = session['user_id']
    user_manager.current_username = session['username']

    repos = getTrendy()
    return render_template('home.html', repos=repos)

@app.route('/search')
# Search route; handles repository search queries
def search_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get("q", "")
    results = search(query) if query else []
    return render_template('search.html', results=results, query=query)

@app.route('/profile')
# User profile; displays user info, search history, and bookmarks
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_info = user_manager.get_user_info()
    history = user_manager.get_search_history()
    bookmarks = user_manager.get_bookmarks()

    return render_template('profile.html', user=user_info, history=history, bookmarks=bookmarks)

@app.route('/logout')
# Logout route; clears session and redirects to login
def logout():
    user_manager.logout()
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))

@app.route('/repo/<path:repo_name>', methods=['GET', 'POST'])
# Repository analysis page; shows metadata and allows bookmarking
def repo_analysis(repo_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Determine data source: POST from search or GET with query params after bookmark toggle
    data = request.form if request.method == 'POST' else request.args
    full_name = data.get('full_name', repo_name)
    owner = data.get('owner', full_name.split('/', 1)[0])
    name = data.get('name', full_name.split('/', 1)[1] if '/' in full_name else full_name)
    description = data.get('description', '')
    url = data.get('url', '')
    stars = data.get('stars', '')
    forks = data.get('forks', '')
    updated_at = data.get('updated_at', '')

    user_manager.add_to_search_history(search_type='Click', repo_name=full_name)

    # Build repo_data
    # If metadata missing (e.g., via profile bookmark), fetch from GitHub API
    if not (description and stars and forks and updated_at):
        try:
            import requests
            resp = requests.get(f"https://api.github.com/repos/{full_name}")
            if resp.status_code == 200:
                repo_json = resp.json()
                description = description or repo_json.get('description', '')
                stars = stars or repo_json.get('stargazers_count', '')
                forks = forks or repo_json.get('forks_count', '')
                updated_at = updated_at or repo_json.get('updated_at', '')
        except Exception as e:
            print(f"Error fetching metadata: {e}")
    repo_data = {
        'name': name,
        'owner': owner,
        'full_name': full_name,
        'description': description,
        'url': url,
        'stars': stars,
        'forks': forks,
        'updated_at': time_ago(updated_at)
    }

    bookmarks = user_manager.get_bookmarks()
    return render_template('repo_analysis.html', repo=repo_data, bookmarks=bookmarks)

    # API Routes for repository analysis
@app.route('/api/summarize', methods=['POST'])
# API: Summarize repository content using LLM and return Markdown and HTML
def api_summarize():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = request.get_json()
    repo_name = data.get('repo_name')
    
    # Raw markdown response from LLM
    summary_md = user_manager.summarize_repo(repo_name)

    # HTML conversion
    summary_html = markdown.markdown(
        summary_md,
        extensions=['fenced_code', 'tables', 'codehilite']
    )
    
    return jsonify({
        'success': True,
        'summary_md': summary_md,
        'summary_html': summary_html
    })

@app.route('/api/file-tree', methods=['POST'])
# API: Retrieve file tree structure for a given repository path
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
# API: Scan a file content using LLM and return Markdown and HTML results
def api_scan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = request.get_json()
    repo_name = data.get('repo_name')
    file_path = data.get('file_path')
    
    # Raw markdown response from LLM
    scan_results_md = user_manager.scan_file(repo_name, file_path)

    # HTML conversion
    scan_results_html = markdown.markdown(
        scan_results_md,
        extensions=['fenced_code', 'tables', 'codehilite']
    )
    
    return jsonify({
        'success': True,
        'scan_results_md': scan_results_md,
        'scan_results_html': scan_results_html
    })

@app.route('/api/export_summary/markdown', methods=['POST'])
# API: Export summary as Markdown file download
def export_summary_md():
    data = request.get_json()
    # receive pre-generated markdown content
    summary_md = data.get('content', '')
    response = make_response(summary_md)
    response.headers['Content-Type'] = 'text/markdown'
    response.headers['Content-Disposition'] = 'attachment; filename=summary.md'
    return response

@app.route('/api/export_summary/pdf', methods=['POST'])
# API: Export summary as PDF by converting Markdown using markdown-pdf
def export_summary_pdf():
    data = request.get_json()
    # receive pre-generated markdown content
    summary_md = data.get('content', '')
    # write markdown to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as md_file:
        md_file.write(summary_md.encode('utf-8'))
        md_path = md_file.name
    pdf_path = md_path.replace('.md', '.pdf')
    try:
        subprocess.run(['npx', 'markdown-pdf', md_path, '-o', pdf_path], check=True)
        return send_file(pdf_path, as_attachment=True, download_name='summary.pdf')
    finally:
        os.remove(md_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

@app.route('/api/export_scan/markdown', methods=['POST'])
# API: Export scan results as Markdown file download
def export_scan_md():
    data = request.get_json()
    # receive pre-generated markdown content
    scan_md = data.get('content', '')
    response = make_response(scan_md)
    response.headers['Content-Type'] = 'text/markdown'
    response.headers['Content-Disposition'] = 'attachment; filename=scan.md'
    return response

@app.route('/api/export_scan/pdf', methods=['POST'])
# API: Export scan results as PDF file download
def export_scan_pdf():
    data = request.get_json()
    # receive pre-generated markdown content
    scan_md = data.get('content', '')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as md_file:
        md_file.write(scan_md.encode('utf-8'))
        md_path = md_file.name
    pdf_path = md_path.replace('.md', '.pdf')
    try:
        subprocess.run(['npx', 'markdown-pdf', md_path, '-o', pdf_path], check=True)
        return send_file(pdf_path, as_attachment=True, download_name='scan.pdf')
    finally:
        os.remove(md_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

@app.route('/api/bookmark', methods=['POST'])
# API: Bookmark a repository for the current user
def api_bookmark():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = request.get_json()
    repo_name = data.get('repo_name')
    
    return jsonify({
        'success': True,
        'message': f'Repository {repo_name} has been bookmarked successfully'
    })

@app.route('/toggle_bookmark', methods=['POST'])
# Toggle bookmark; handles adding or removing based on form data
def toggle_bookmark():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    action = request.form['action']
    
    if action == 'add':
        repo_name = request.form['repo_name']
        user_manager.add_bookmark(repo_name)
    elif action == 'remove':
        bookmark_id = request.form.get('bookmark_id')
        if bookmark_id and bookmark_id.isdigit():
            user_manager.remove_bookmark(int(bookmark_id))

    # After toggling, redirect back to repo_analysis with full metadata to preserve display
    form = request.form
    full_name = form.get('repo_name', '') or ''
    owner = form.get('repo_owner', '') or ''
    # derive simple name from full_name
    if full_name and '/' in full_name:
        name = full_name.split('/', 1)[1]
    else:
        name = full_name
    description = form.get('description', '') or ''
    repo_url = form.get('repo_url', '') or ''
    stars = form.get('stars', '') or ''
    forks = form.get('forks', '') or ''
    updated_at = form.get('updated_at', '') or ''
    # Redirect back to repo_analysis with metadata as query params
    return redirect(url_for('repo_analysis',
                             repo_name=full_name,
                             full_name=full_name,
                             owner=owner,
                             name=name,
                             description=description,
                             url=repo_url,
                             stars=stars,
                             forks=forks,
                             updated_at=updated_at))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)