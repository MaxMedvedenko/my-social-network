document.querySelector('.hamburger-button').addEventListener('click', function() {
    const navLinks = document.querySelector('.nav-links');
    const hamburgerButton = document.querySelector('.hamburger-button');
    const isMenuOpen = navLinks.style.display === 'block';

    // Перемикання відображення меню
    navLinks.style.display = isMenuOpen ? 'none' : 'block';

    // Перемикання значка кнопки
    if (isMenuOpen) {
        hamburgerButton.innerHTML = '☰'; // Значок гамбургера
    } else {
        hamburgerButton.innerHTML = '&#10005;'; // Значок Х
    }
});
