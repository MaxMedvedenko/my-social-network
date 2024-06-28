// static/js/main.js
function toggleDropdown(element) {
    var dropdownContent = element.nextElementSibling;
    dropdownContent.classList.toggle("show");
}

// Закрити спливаюче меню, якщо користувач натисне поза ним
window.onclick = function(event) {
    if (!event.target.matches('.dots-vertical-svg')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
