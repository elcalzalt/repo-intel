const themeToggle = document.getElementById('themeToggle');
const body = document.body;
const userInfoContainer = document.getElementById('userInfo');
const bookmarksContainer = document.getElementById('bookmarks');
const searchHistoryList = document.getElementById('searchHistoryList');

// ===== Theme Toggle Logic =====
themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark');
    const isDark = body.classList.contains('dark');
    themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// Apply saved theme
if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark');
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
}

// ===== Mock User Info =====
const mockUser = {
    username: 'dev_galaxy',
    bio: 'Passionate full-stack developer. Loves open source and coffee ☕.',
    joined: 'January 2023'
};

userInfoContainer.innerHTML = `
    <h2>@${mockUser.username}</h2>
    <p>${mockUser.bio}</p>
    <small>Joined: ${mockUser.joined}</small>
`;

// ===== Mock Bookmarks =====
const mockBookmarks = [
    {
        name: 'awesome-react',
        description: 'A collection of awesome React resources.',
        stars: 48000
    },
    {
        name: 'machine-learning-roadmap',
        description: 'Step-by-step guide to becoming an ML engineer.',
        stars: 32000
    },
    {
        name: 'css-tips-and-tricks',
        description: 'Useful CSS tips for beautiful UIs.',
        stars: 19000
    }
];

mockBookmarks.forEach(repo => {
    const card = document.createElement('div');
    card.classList.add('repo-card');
    card.innerHTML = `
        <h3>${repo.name}</h3>
        <p>${repo.description}</p>
        <small>⭐ ${repo.stars}</small>
    `;
    bookmarksContainer.appendChild(card);
});

/* ===== Mock Search History ===== */
const mockSearchHistory = [
    "React hooks tutorial",
    "Best Python libraries 2025",
    "How to contribute to open source",
    "CSS grid vs flexbox",
    "Node.js performance tips"
];

mockSearchHistory.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    searchHistoryList.appendChild(li);
});

// Hamburger toggle for nav menu
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');

hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});
