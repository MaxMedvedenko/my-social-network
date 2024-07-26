// Функція для відкриття модального вікна
function openModal(imageSrc) {
    var modal = document.getElementById("imageModal"); // Знаходимо модальне вікно
    var modalImg = document.getElementById("modalImage"); // Знаходимо зображення в модальному вікні

    modal.style.display = "block"; // Відображаємо модальне вікно
    modalImg.src = imageSrc; // Встановлюємо джерело зображення

    // Закриття модального вікна при натисканні за межами зображення
    modal.onclick = function(event) {
        if (event.target !== modalImg) {
            modal.style.display = "none";
        }
    };
}

// Функція для закриття модального вікна
function closeModal() {
    var modal = document.getElementById("imageModal");
    modal.style.display = "none";
}
