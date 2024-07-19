//--- for popup menu ---//

document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.dots-vertical-svg');

    toggleButtons.forEach(toggleButton => {
        const dropdownContent = toggleButton.nextElementSibling;

        toggleButton.addEventListener('click', function() {
            dropdownContent.style.display = (dropdownContent.style.display === 'block') ? 'none' : 'block';
        });

        document.addEventListener('click', function(e) {
            if (!dropdownContent.contains(e.target) && e.target !== toggleButton) {
                dropdownContent.style.display = 'none';
            }
        });
    });
});