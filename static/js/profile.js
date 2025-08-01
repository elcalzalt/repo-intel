const userInfoContainer = document.getElementById('userInfo');
const bookmarksContainer = document.getElementById('bookmarks');
const searchHistoryList = document.getElementById('searchHistoryList');

// ===== Mock User Info =====
// const mockUser = {
//     username: 'dev_galaxy',
//     bio: 'Passionate full-stack developer. Loves open source and coffee ☕.',
//     joined: 'January 2023'
// };

// userInfoContainer.innerHTML = `
//     <h3>@${mockUser.username}</h3>
//     <p>${mockUser.bio}</p>
//     <small>Joined: ${mockUser.joined}</small>
// `;

// ===== Mock Bookmarks =====
// const mockBookmarks = [
//     {
//         name: 'awesome-react',
//         description: 'A collection of awesome React resources.',
//         stars: 48000
//     },
//     {
//         name: 'machine-learning-roadmap',
//         description: 'Step-by-step guide to becoming an ML engineer.',
//         stars: 32000
//     },
//     {
//         name: 'css-tips-and-tricks',
//         description: 'Useful CSS tips for beautiful UIs.',
//         stars: 19000
//     }
// ];

// mockBookmarks.forEach(repo => {
//     const card = document.createElement('div');
//     card.classList.add('repo-card');
//     card.innerHTML = `
//         <h3>${repo.name}</h3>
//         <p>${repo.description}</p>
//         <small>⭐ ${repo.stars}</small>
//     `;
//     bookmarksContainer.appendChild(card);
// });

/* ===== Mock Search History ===== */
// const mockSearchHistory = [
//     "React hooks tutorial",
//     "Best Python libraries 2025",
//     "How to contribute to open source",
//     "CSS grid vs flexbox",
//     "Node.js performance tips"
// ];

// mockSearchHistory.forEach(item => {
//     const li = document.createElement('li');
//     li.textContent = item;
//     searchHistoryList.appendChild(li);
// });