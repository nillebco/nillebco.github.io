let translations = {};
const defaultLocale = 'en';
const supportedLocales = ['en', 'fr'];

// Function to load translations
async function loadTranslations(locale) {
    try {
        const response = await fetch(`/locales/${locale}.json`);
        translations = await response.json();
        applyTranslations();
        // Update HTML lang attribute
        document.documentElement.lang = locale;
        
        // Call page-specific translation function if it exists
        if (typeof window.applyPageTranslations === 'function') {
            window.applyPageTranslations(locale);
        }
    } catch (error) {
        console.error('Error loading translations:', error);
        // Fallback to English if translation loading fails
        if (locale !== defaultLocale) {
            loadTranslations(defaultLocale);
        }
    }
}

// Function to apply translations to the page
function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[key]) {
            element.textContent = translations[key];
        }
    });
}

// Function to get language from URL query parameter
function getLanguageFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const langParam = urlParams.get('lang');
    return langParam && supportedLocales.includes(langParam) ? langParam : null;
}

// Function to get browser language
function getBrowserLanguage() {
    const language = navigator.language || navigator.userLanguage;
    const baseLanguage = language.split('-')[0];
    return supportedLocales.includes(baseLanguage) ? baseLanguage : defaultLocale;
}

// Function to get the preferred language
function getPreferredLanguage() {
    return getLanguageFromURL() || getBrowserLanguage();
}

// Initialize localization
document.addEventListener('DOMContentLoaded', () => {
    const locale = getPreferredLanguage();
    loadTranslations(locale);
}); 