# 🔍 Repo Intel

> An intelligent GitHub repository analysis platform powered by AI that helps developers discover, analyze, and understand open-source projects with ease.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.1.1-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Overview

**Repo Intel** is a full-stack web application that transforms how developers interact with GitHub repositories. By leveraging AI-powered analysis through Google's Gemini API, it provides intelligent insights, vulnerability scanning, and comprehensive summaries of any public GitHub repository. The platform features advanced search capabilities, user authentication, bookmarking functionality, and an intuitive interface for exploring the open-source ecosystem.

### Why Repo Intel?

- **Time-Saving**: Get instant AI-generated summaries instead of manually reading through documentation
- **Security-First**: Automated vulnerability scanning helps identify potential security issues
- **Smart Discovery**: Advanced filtering and trending repositories help you find relevant projects faster
- **Knowledge Base**: Ask questions about specific files and get AI-powered answers
- **Personal Library**: Bookmark and track repositories you're interested in

## ✨ Key Features

### 🤖 AI-Powered Analysis
- **Repository Summarization**: Generates comprehensive summaries including project purpose, latest commits, and open issues
- **Vulnerability Scanning**: Analyzes code files for potential security vulnerabilities and code quality issues
- **Interactive Q&A**: Ask specific questions about any file in a repository and receive detailed explanations

### 🔎 Advanced Search & Discovery
- **Multi-Parameter Search**: Filter by language, stars, forks, size, license, topics, and more
- **Trending Repositories**: Discover the most popular repositories from the last 6 months
- **Category-Based Navigation**: Quick access to repositories in Web Dev, AI, Mobile, Data Science, Security, and Game Development

### 👤 User Management
- **Secure Authentication**: Password hashing with salt for secure user accounts
- **Search History**: Track all your repository analyses and scans
- **Bookmark System**: Save favorite repositories for quick access
- **Personalized Dashboard**: View your activity and saved repositories

### 🎨 Modern UI/UX
- **Responsive Design**: Seamless experience across desktop, tablet, and mobile devices
- **Dark Mode**: Eye-friendly dark theme option
- **Interactive File Trees**: Navigate repository structures with visual feedback
- **Loading Animations**: Engaging progress indicators for AI operations
- **Export Functionality**: Download analysis results as Markdown or PDF

### ⚡ Performance Optimization
- **Intelligent Caching**: Database-backed caching system reduces redundant API calls
- **Time-Based Cache Invalidation**: Automatically refreshes stale data
- **Efficient Database Design**: Optimized SQLAlchemy models for fast queries

## 🛠 Technology Stack

### Backend
- **Framework**: Flask 3.1.1 (Python web framework)
- **Database**: SQLAlchemy with SQLite (easily portable to PostgreSQL/MySQL)
- **API Integration**: 
  - GitHub REST API for repository data
  - Google Gemini AI (gemini-2.5-flash) for intelligent analysis
- **Authentication**: Custom implementation with SHA-256 password hashing
- **Document Processing**: Markdown parsing and PDF generation

### Frontend
- **HTML5 & CSS3**: Modern, semantic markup with custom styling
- **JavaScript (ES6+)**: Vanilla JS for interactive features
- **Font Awesome**: Icon library for enhanced UI
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox

### Key Libraries & Dependencies
```
Flask==3.1.1                 # Web framework
SQLAlchemy==2.0.41          # ORM and database toolkit
google-genai==1.25.0        # Google's Gemini AI SDK
requests==2.32.4            # HTTP library for API calls
Markdown==3.8.2             # Markdown to HTML conversion
markdown-pdf==1.7           # PDF export functionality
PyMuPDF==1.25.3            # PDF processing
Werkzeug==3.1.3            # WSGI utilities
```

## 🏗 Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                      │
│  (HTML/CSS/JS - Responsive, Dark Mode, Animations)     │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                   Flask Application                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Routes &   │  │    User      │  │   Export     │ │
│  │  Controllers │  │  Management  │  │   Handlers   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                  Business Logic Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   GitHub     │  │      AI      │  │    Cache     │ │
│  │   Client     │  │   Analyzer   │  │   Manager    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│               Data Persistence Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │    Users     │  │    Cache     │  │  Bookmarks & │ │
│  │   Database   │  │   Database   │  │   History    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────┐
│                  External Services                       │
│  ┌──────────────┐           ┌──────────────┐           │
│  │   GitHub     │           │  Google      │           │
│  │   REST API   │           │  Gemini AI   │           │
│  └──────────────┘           └──────────────┘           │
└─────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. **User Manager** (`user_manager.py`)
Handles all user-related operations including authentication, session management, search history, and bookmarks.

#### 2. **GitHub Client** (`github_client.py`)
Interfaces with GitHub's REST API to fetch repository data, file contents, commits, and issues.

#### 3. **AI Analyzer** (`ai_analyzer.py`)
Integrates with Google's Gemini AI to generate summaries, scan for vulnerabilities, and answer questions.

#### 4. **Cache Database** (`cache_db.py`)
Implements intelligent caching with time-based invalidation to optimize API usage and response times.

#### 5. **Flask Application** (`app.py`)
Main application entry point that routes requests and coordinates between components.

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Node.js and npm (for PDF export functionality)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/repo-intel.git
   cd repo-intel
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies (for PDF export)**
   ```bash
   npm install -g markdown-pdf
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GENAI_KEY=your_google_gemini_api_key_here
   GITHUB_TOKEN=your_github_personal_access_token_here
   FLASK_SECRET_KEY=your_secret_key_here
   ```

6. **Initialize the database**
   ```bash
   python -c "from user_manager import UserManager; from cache_db import CacheDatabase; UserManager(CacheDatabase())"
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   Open your browser and navigate to `http://localhost:8080`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GENAI_KEY` | Google Gemini API key for AI analysis | Yes |
| `GITHUB_TOKEN` | GitHub Personal Access Token (increases rate limits) | Recommended |
| `FLASK_SECRET_KEY` | Secret key for Flask session management | Yes |

### Getting API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

#### GitHub Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `public_repo`, `read:user`
4. Copy the token to your `.env` file

### Database Configuration

By default, the application uses SQLite databases:
- `users.db` - User accounts and authentication
- `cache.db` - Repository summaries and scan results

To use PostgreSQL or MySQL, modify the connection strings in:
- `user_manager.py`: `db_path` parameter
- `cache_db.py`: `db_path` parameter

## 🚀 Usage

### For Regular Users

1. **Register an Account**
   - Navigate to `/register`
   - Fill in username, email, and password
   - Submit to create your account

2. **Login**
   - Go to `/login`
   - Enter your credentials
   - Access the main dashboard

3. **Search for Repositories**
   - Use the search bar on the home page
   - Apply advanced filters (language, stars, forks, etc.)
   - Browse trending repositories

4. **Analyze a Repository**
   - Click on any repository card
   - Choose from available analysis options:
     - Generate AI Summary
     - Scan Files for Vulnerabilities
     - Ask Questions about specific files
   - Bookmark repositories for later

5. **View Your Profile**
   - Access saved bookmarks
   - Review search history
   - Manage your account

### For Developers

#### Running Tests
```bash
# Run all unit tests
python -m unittest discover -s unittests -p "test_*.py"

# Run specific test file
python -m unittest unittests/test_user_manager.py

# Run with verbose output
python -m unittest discover -s unittests -p "test_*.py" -v
```

#### API Endpoints

##### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

##### Repository Analysis
- `POST /api/summarize` - Generate AI summary
- `POST /api/scan` - Scan file for vulnerabilities
- `POST /api/question` - Ask question about a file
- `POST /api/file-tree` - Get repository file structure

##### User Features
- `POST /api/bookmark` - Bookmark a repository
- `POST /toggle_bookmark` - Add/remove bookmark
- `GET /profile` - View user profile

##### Export
- `POST /api/export_summary/markdown` - Export summary as MD
- `POST /api/export_summary/pdf` - Export summary as PDF
- `POST /api/export_scan/markdown` - Export scan results as MD
- `POST /api/export_scan/pdf` - Export scan results as PDF

## 🧪 Testing

The project includes comprehensive unit tests covering all major components:

### Test Coverage

- **User Management**: Authentication, registration, session handling
- **Database Operations**: CRUD operations, caching logic
- **GitHub Integration**: API calls, data parsing, error handling
- **AI Analysis**: Summary generation, vulnerability scanning

### Running Tests

```bash
# Install test dependencies (if not already installed)
pip install -r requirements.txt

# Run all tests
python -m unittest discover -s unittests

# Run with coverage (if pytest-cov is installed)
pytest --cov=. --cov-report=html unittests/
```

## 📁 Project Structure

```
repo-intel/
├── app.py                      # Main Flask application
├── user_manager.py             # User authentication & management
├── github_client.py            # GitHub API integration
├── ai_analyzer.py              # AI analysis with Gemini
├── cache_db.py                 # Caching system
├── home.py                     # Home page logic & search
├── time_ago.py                 # Time formatting utility
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
│
├── static/                     # Static assets
│   ├── css/
│   │   ├── auth.css           # Authentication pages
│   │   ├── home.css           # Home page & layout
│   │   ├── profile.css        # User profile
│   │   ├── repo_analysis.css  # Repository analysis
│   │   ├── search.css         # Search results
│   │   └── styles.css         # Global styles
│   └── js/
│       ├── auth.js            # Authentication logic
│       ├── home.js            # Home page interactions
│       └── profile.js         # Profile page logic
│
├── templates/                  # HTML templates
│   ├── layout.html            # Base template
│   ├── home.html              # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── profile.html           # User profile
│   ├── search.html            # Search results
│   └── repo_analysis.html     # Repository analysis
│
├── unittests/                  # Unit tests
│   ├── test_ai.py             # AI analyzer tests
│   ├── test_database.py       # Database tests
│   ├── test_github.py         # GitHub client tests
│   └── test_user_manager.py   # User manager tests
│
├── summary_instruction.txt     # AI prompt for summaries
├── scan_instruction.txt        # AI prompt for scans
└── qna_instruction.txt         # AI prompt for Q&A
```

## 📸 Screenshots

### Home Page
*Discover trending repositories and use advanced search filters*

### Repository Analysis
*AI-powered summaries and vulnerability scanning*

### User Profile
*Track your search history and manage bookmarks*

### Dark Mode
*Eye-friendly dark theme for extended usage*

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write unit tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 🔒 Security Considerations

- Passwords are hashed using SHA-256 with unique salts
- SQL injection prevention through SQLAlchemy ORM
- XSS protection via template escaping
- CSRF protection on forms
- Environment variables for sensitive data
- Session management with secure cookies

## 🐛 Known Issues & Future Enhancements

### Known Issues
- PDF export requires Node.js and markdown-pdf installed globally
- Large repositories may take longer to analyze
- GitHub API rate limits apply (60 requests/hour without authentication)

### Planned Features
- [ ] OAuth integration for GitHub login
- [ ] Support for private repositories
- [ ] Comparative analysis of multiple repositories
- [ ] Repository health scoring system
- [ ] Team collaboration features
- [ ] CI/CD integration analysis
- [ ] Docker containerization
- [ ] API rate limit monitoring dashboard

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Authors

- [@elcalzalt](https://github.com/elcalzalt)
- [@Mustafa-Tahir0](https://github.com/Mustafa-Tahir0)
- [@Angelal78](https://github.com/Angelal78)
- [@abigaelod](https://github.com/abigaelod)

## 🙏 Acknowledgments

- [GitHub API](https://docs.github.com/en/rest) for repository data
- [Google Gemini](https://ai.google.dev/) for AI-powered analysis
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Font Awesome](https://fontawesome.com/) for icons
- Open source community for inspiration and support

---

<div align="center">

**If you find this project useful, please consider giving it a ⭐!**

Made with ❤️ and Python

</div>
