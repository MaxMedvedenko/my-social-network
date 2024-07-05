// document.addEventListener('DOMContentLoaded', function() {
//     // Select all elements with the class 'dots-vertical-svg'
//     const toggleButtons = document.querySelectorAll('.dots-vertical-svg');
  
//     // Add event listeners to each toggle button
//     toggleButtons.forEach(function(toggleButton) {
//       toggleButton.addEventListener('click', function(e) {
//         e.stopPropagation(); // Stop the event from bubbling up to the document
  
//         // Find the corresponding dropdown-content element
//         const popupMenu = toggleButton.nextElementSibling;
  
//         // Toggle the display of the popup menu
//         if (popupMenu.style.display === 'none' || popupMenu.style.display === '') {
//           // Close any open popup menus
//           document.querySelectorAll('.dropdown-content').forEach(function(menu) {
//             menu.style.display = 'none';
//           });
//           // Open the current popup menu
//           popupMenu.style.display = 'block';
//         } else {
//           // Close the current popup menu
//           popupMenu.style.display = 'none';
//         }
//       });
//     });
//   });
  
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('dots-vertical-svg');
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