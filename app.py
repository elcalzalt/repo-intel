from flask import Flask, render_template, request, jsonify
from home import *

app = Flask(__name__)

@app.route('/')
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

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/repo/<path:repo_name>')
def repo_analysis(repo_name):
    # Extract owner and repo name from the path
    if '/' in repo_name:
        owner, name = repo_name.split('/', 1)
    else:
        # Fallback if no owner specified
        owner = "unknown"
        name = repo_name
    
    # Mock repo data - in real implementation, fetch from GitHub API
    repo_data = {
        'name': name,
        'owner': owner,
        'full_name': repo_name,
        'description': f'Repository {name} by {owner}',
        'url': f'https://github.com/{repo_name}',
        'stars': '1.2k',
        'forks': '345',
        'language': 'Python',
        'updated_at': '2 days ago'
    }
    
    return render_template('repo_analysis.html', repo=repo_data)

# API Routes for repository analysis
@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    data = request.get_json()
    repo_url = data.get('repo_url')
    repo_name = data.get('repo_name')
    
    # Mock summary - replace with actual AI analysis
    summary = f"""
    This repository '{repo_name}' appears to be a well-structured project with the following characteristics:
    
    🎯 Purpose: The repository serves as a comprehensive solution for repository analysis and insights.
    
    📁 Structure: 
    - Well-organized codebase with clear separation of concerns
    - Includes proper documentation and setup instructions
    - Follows modern development practices
    
    🔧 Key Features:
    - Repository search and discovery
    - Automated code analysis
    - Security scanning capabilities
    - User-friendly web interface
    
    📊 Assessment: This is an active project with regular updates and good maintenance practices.
    """
    
    return jsonify({
        'success': True,
        'summary': summary.strip()
    })

@app.route('/api/scan', methods=['POST'])
def api_scan():
    data = request.get_json()
    repo_url = data.get('repo_url')
    repo_name = data.get('repo_name')
    
    # Mock scan results - replace with actual security scanning
    scan_results = {
        'issues': [
            {'severity': 'low', 'message': 'Consider adding more comprehensive error handling'},
            {'severity': 'medium', 'message': 'Some dependencies may have newer versions available'}
        ],
        'security_warnings': [
            'No critical security vulnerabilities detected',
            'All dependencies appear to be up to date'
        ]
    }
    
    return jsonify({
        'success': True,
        'scan_results': scan_results
    })

@app.route('/api/bookmark', methods=['POST'])
def api_bookmark():
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