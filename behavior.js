function setupToastMenu() {
  var toastButton = document.querySelector('.toast-button button');
  var toastMenu = document.getElementById('toast-menu');
  toastButton.addEventListener('click', () => {
    toastMenu.classList.toggle('hidden');
  });
}
function setupThemeToggle() {
  const toggleButton = document.getElementById('theme-button');
  toggleButton.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    themeIcon = document.getElementById('theme-icon');
    if (document.body.classList.contains('dark-mode')) {
      themeIcon.classList.remove('fa-moon');
      themeIcon.classList.add('fa-sun');
    } else {
      themeIcon.classList.remove('fa-sun');
      themeIcon.classList.add('fa-moon');
    }
  });
}
function setupCopyrightNotice() {
  document.getElementById('copyright-notice').innerHTML = '&copy; 2022-' + new Date().getFullYear() + ' Ivo Bellin Salarin';
}