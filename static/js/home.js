const searchInput = document.getElementById('searchInput');
const suggestions = document.getElementById('suggestions');
const repoCards = document.getElementById('repoCards');

// Mock repo data for search suggestions
const mockRepos = [
    { name: 'awesome-python', stars: 100000, description: 'A curated list of awesome Python frameworks.' },
    { name: 'freeCodeCamp', stars: 350000, description: 'Learn to code for free.' },
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

// Search suggestions functionality
if (searchInput && suggestions) {
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

        // Display suggestions
        filtered.slice(0, 5).forEach(repo => {
            const li = document.createElement('li');
            li.textContent = repo.name;
            li.addEventListener('click', () => {
                searchInput.value = repo.name;
                suggestions.style.display = 'none';
            });
            suggestions.appendChild(li);
        });

        suggestions.style.display = 'block';
    });

    // Hide suggestions when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-wrapper')) {
            suggestions.style.display = 'none';
        }
    });
}
