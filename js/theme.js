// Theme handling
const THEME_DARK = 'dark-mode';
const THEME_LIGHT = 'light-mode';
const THEME_KEY = 'theme-preference';

// Function to get theme from URL query parameter
function getThemeFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const themeParam = urlParams.get('theme');
    return themeParam === 'dark' ? THEME_DARK : 
           themeParam === 'light' ? THEME_LIGHT : 
           null;
}

// Function to get system theme preference
function getSystemThemePreference() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 
           THEME_DARK : THEME_LIGHT;
}

// Function to get stored theme preference
function getStoredThemePreference() {
    return localStorage.getItem(THEME_KEY);
}

// Function to set theme preference
function setThemePreference(theme) {
    localStorage.setItem(THEME_KEY, theme);
    applyTheme(theme);
}

// Function to apply theme
function applyTheme(theme) {
    document.body.classList.remove(THEME_DARK, THEME_LIGHT);
    document.body.classList.add(theme);
}

// Function to toggle theme
function toggleTheme() {
    const currentTheme = document.body.classList.contains(THEME_DARK) ? THEME_DARK : THEME_LIGHT;
    const newTheme = currentTheme === THEME_DARK ? THEME_LIGHT : THEME_DARK;
    setThemePreference(newTheme);
}

function currentTheme() {
    const theme = getThemeFromURL() || 
                 getStoredThemePreference() || 
                 getSystemThemePreference();
    return theme;
}

// Function to initialize theme
function initializeTheme() {    
    applyTheme(currentTheme());

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)')
        .addEventListener('change', (e) => {
            if (!getStoredThemePreference() && !getThemeFromURL()) {
                applyTheme(e.matches ? THEME_DARK : THEME_LIGHT);
            }
        });
}

// Initialize theme when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeTheme); 