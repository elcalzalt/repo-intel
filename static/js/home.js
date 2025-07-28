// Wait for DOM to be fully loaded before executing
document.addEventListener('DOMContentLoaded', function() {
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

    // Initialize filter elements with null checks
    const filterToggle = document.querySelector('.filter-toggle');
    const advancedFilters = document.getElementById('advancedFilters');
    const applyFiltersBtn = document.querySelector('.apply-filters');
    const searchForm = document.getElementById('searchForm');
    const languageSelect = document.getElementById('language');
    const starsSelect = document.getElementById('stars');
    const updatedSelect = document.getElementById('updated');

    // Debugging logs
    console.log('Filter elements initialized:', {
        filterToggle,
        advancedFilters,
        applyFiltersBtn,
        searchForm,
        languageSelect,
        starsSelect,
        updatedSelect
    });

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

    // Enhanced filter toggle functionality
    function toggleFilters(e) {
        if (e) {
            e.stopPropagation(); // Prevent event bubbling
            e.preventDefault(); // Prevent default behavior
        }

        if (!advancedFilters) {
            console.error('Advanced filters element not found');
            return;
        }

        advancedFilters.classList.toggle('show');
        console.log('Filters visibility:', advancedFilters.classList.contains('show'));

        // Close suggestions when opening filters
        if (suggestions && advancedFilters.classList.contains('show')) {
            suggestions.style.display = 'none';
        }
    }

    // Initialize filter toggle with better event handling
    if (filterToggle) {
        filterToggle.addEventListener('click', toggleFilters);
        console.log('Filter toggle event listener added');
    } else {
        console.error('Filter toggle button not found');
    }

    // Close filters when clicking outside
    document.addEventListener('click', function(event) {
        if (!advancedFilters) return;

        const isClickInsideFilters = advancedFilters.contains(event.target);
        const isClickOnToggle = event.target === filterToggle ||
            (filterToggle && filterToggle.contains(event.target));

        if (!isClickInsideFilters && !isClickOnToggle) {
            advancedFilters.classList.remove('show');
            console.log('Filters hidden (click outside)');
        }
    });

    // Enhanced form submission with filters
    if (applyFiltersBtn && searchForm) {
        applyFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Apply filters clicked');

            // Verify all required elements exist
            if (!searchInput || !languageSelect || !starsSelect || !updatedSelect) {
                console.error('Required form elements missing');
                return;
            }

            // Set values in hidden form
            document.getElementById('hiddenSearchInput').value = searchInput.value;
            document.getElementById('hiddenLanguage').value = languageSelect.value;
            document.getElementById('hiddenStars').value = starsSelect.value;
            document.getElementById('hiddenUpdated').value = updatedSelect.value;

            console.log('Form values set:', {
                q: searchInput.value,
                language: languageSelect.value,
                stars: starsSelect.value,
                updated: updatedSelect.value
            });

            // Submit the form
            searchForm.submit();
        });
    } else {
        console.error('Apply filters button or search form not found');
    }

    // Handle pressing Enter in search input to submit with filters
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                console.log('Enter pressed in search input');

                // If filters are open, apply them
                if (advancedFilters && advancedFilters.classList.contains('show')) {
                    if (applyFiltersBtn) {
                        applyFiltersBtn.click();
                    }
                } else {
                    // Regular search without filters
                    document.getElementById('hiddenSearchInput').value = searchInput.value;
                    document.getElementById('hiddenLanguage').value = '';
                    document.getElementById('hiddenStars').value = '';
                    document.getElementById('hiddenUpdated').value = '';
                    searchForm.submit();
                }
            }
        });
    }

    // Close filters when pressing Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && advancedFilters && advancedFilters.classList.contains('show')) {
            advancedFilters.classList.remove('show');
            console.log('Filters hidden (Escape key)');
        }
    });

    // Additional debugging
    console.log('Home.js initialized successfully');
});