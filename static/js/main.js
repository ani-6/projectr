// --- Sidebar Toggle Logic ---
function toggleSidebar() {
    const sidebar = document.getElementById('sidebarMenu');
    const overlay = document.getElementById('sidebarOverlay');

    if (sidebar.classList.contains('show')) {
        sidebar.classList.remove('show');
        overlay.classList.remove('show');
    } else {
        sidebar.classList.add('show');
        overlay.classList.add('show');
    }
}

// --- Mobile Search Toggle Logic ---
function toggleSearch() {
    const searchBar = document.getElementById('mobileSearchBar');
    if (searchBar.classList.contains('d-none')) {
        searchBar.classList.remove('d-none');
        // Optional: Auto focus the input when opened
        const input = searchBar.querySelector('input');
        if (input) input.focus();
    } else {
        searchBar.classList.add('d-none');
    }
}

// --- Dark/Light Mode Logic ---
const toggleButton = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const htmlElement = document.documentElement;

function updateIcon(theme) {
    if (theme === 'dark') {
        themeIcon.className = 'fa-solid fa-sun';
    } else {
        themeIcon.className = 'fa-solid fa-moon';
    }
}

function setTheme(theme, saveToStorage = false) {
    htmlElement.setAttribute('data-bs-theme', theme);
    updateIcon(theme);
    if (saveToStorage) {
        localStorage.setItem('theme', theme);
    }
}

// 1. Check for saved preference
const savedTheme = localStorage.getItem('theme');
const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)');

if (savedTheme) {
    setTheme(savedTheme, false);
} else {
    // 2. If no save, use system preference (and don't save to storage yet)
    setTheme(systemPrefersDark.matches ? 'dark' : 'light', false);
}

// 3. Listen for system changes (only applies if no manual override exists)
systemPrefersDark.addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'light', false);
    }
});

// 4. Toggle button (Manual override)
if (toggleButton) {
    toggleButton.addEventListener('click', () => {
        const currentTheme = htmlElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme, true); // Save to storage as manual override
    });
}

// --- Initialize Toasts (Auto-Show) ---
document.addEventListener('DOMContentLoaded', function () {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl)
    })
    toastList.forEach(toast => toast.show());
});