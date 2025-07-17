const searchInput = document.getElementById('searchInput');
const suggestions = document.getElementById('suggestions');
const repoCards = document.getElementById('repoCards');
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Mock repo data
const mockRepos = [
    { name: 'awesome-python', stars: 100000, description: 'A curated list of awesome Python frameworks.' },
    { name: 'freeCodeCamp', stars: 350000, description: 'Learn to code for free.' },
    { name: '30-seconds-of-code', stars: 100000, description: 'Short JavaScript code snippets.' },
    { name: 'react', stars: 200000, description: 'A JavaScript library for building user interfaces.' },
    { name: 'vue', stars: 210000, description: 'The Progressive JavaScript Framework.' },
    { name: 'tensorflow', stars: 170000, description: 'An end-to-end open source machine learning platform.' },
    { name: 'django', stars: 66000, description: 'The Web framework for perfectionists with deadlines.' },
    { name: 'flask', stars: 60000, description: 'A lightweight WSGI web application framework.' },
    { name: 'linux', stars: 140000, description: 'Linux kernel source tree.' },
    { name: 'node', stars: 95000, description: 'Node.js JavaScript runtime.' },
    { name: 'kubernetes', stars: 100000, description: 'Production-Grade Container Scheduling and Management.' },
    { name: 'flutter', stars: 125000, description: 'UI toolkit for building natively compiled applications.' },
];

// Render repo cards inside carousel container
mockRepos.forEach(repo => {
    const card = document.createElement('div');
    card.classList.add('repo-card');
    card.style.cursor = 'pointer'; // Make it clear it's clickable
    card.innerHTML = `
    <h3>${repo.name}</h3>
    <p>${repo.description}</p>
    <small>⭐ ${repo.stars.toLocaleString()}</small>
  `;
  
    // Add click event to redirect to summary page
    card.addEventListener('click', () => {
        const repoUrl = `https://github.com/${repo.name.includes('/') ? repo.name : 'microsoft/' + repo.name}`;
        window.location.href = `summary.html?repo=${encodeURIComponent(repoUrl)}`;
    });
    
    repoCards.appendChild(card);
});

// Search suggestions
searchInput.addEventListener('input', () => {
    const input = searchInput.value.toLowerCase();
    suggestions.innerHTML = '';

    if (!input) {
        suggestions.style.display = 'none';
        return;
    }

    const filtered = mockRepos.filter(repo => repo.name.toLowerCase().includes(input));

    if (filtered.length === 0) {
        suggestions.style.display = 'none';
        return;
    }

    filtered.forEach(repo => {
        const li = document.createElement('li');
        li.textContent = repo.name;
        li.style.cursor = 'pointer';
        li.onclick = () => {
            const repoUrl = `https://github.com/${repo.name.includes('/') ? repo.name : 'microsoft/' + repo.name}`;
            window.location.href = `summary.html?repo=${encodeURIComponent(repoUrl)}`;
            suggestions.style.display = 'none';
            searchInput.value = repo.name;
        };
        suggestions.appendChild(li);
    });

    suggestions.style.display = 'block';
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-wrapper')) {
        suggestions.style.display = 'none';
    }
});


// Hamburger toggle for nav menu
hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// Theme toggle with localStorage
themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark');
    const isDark = body.classList.contains('dark');
    themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// Load saved theme
if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark');
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
}
