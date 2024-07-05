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



//--- for edit comment ---//

document.addEventListener('DOMContentLoaded', function() {
    // Додавання обробки подій для клікабельних посилань для редагування коментарів
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('edit-comment-link')) {
            e.preventDefault();
            const commentId = e.target.getAttribute('data-comment-id');
            const commentElement = document.getElementById(`comment-${commentId}`);
            const commentContentElement = commentElement.querySelector('.comment-content');

            // Якщо вже відображається форма редагування, перестаємо обробляти клік
            if (commentElement.classList.contains('editing')) {
                return;
            }

            // Збереження оригінального вмісту коментаря
            const originalContent = commentContentElement.textContent.trim();

            // Показ форми редагування
            const editCommentForm = document.createElement('form');
            editCommentForm.classList.add('edit-comment-form');
            editCommentForm.setAttribute('id', `edit-comment-form-${commentId}`);

            const textarea = document.createElement('textarea');
            textarea.classList.add('comment-textarea');
            textarea.setAttribute('name', 'content');
            textarea.setAttribute('rows', '4');
            textarea.style.width = '100%';
            textarea.style.padding = '10px';
            textarea.style.border = '1px solid #ddd';
            textarea.style.borderRadius = '5px';
            textarea.style.marginBottom = '10px';
            textarea.style.maxWidth = '1090px';
            textarea.textContent = originalContent;

            editCommentForm.appendChild(textarea);

            const saveButton = document.createElement('button');
            saveButton.setAttribute('type', 'submit');
            saveButton.classList.add('edit-comment-btn');
            saveButton.textContent = 'Save';

            editCommentForm.appendChild(saveButton);

            commentContentElement.innerHTML = ''; // Очистка вмісту коментаря
            commentContentElement.appendChild(editCommentForm);

            // Додаємо обробник подій для відправки форми через AJAX
            editCommentForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);

                fetch(`/comment/${commentId}/edit/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'), // Отримання CSRF-токена
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        // Оновлення вмісту коментаря на сторінці
                        commentContentElement.textContent = formData.get('content');
                        commentElement.classList.remove('editing'); // Позначаємо, що редагування завершено
                    } else {
                        console.error('Error updating comment:', data.error);
                        // Обробка помилки
                    }
                })
                .catch(error => console.error('Error updating comment:', error));
            });
        }
    });

    // Функція для отримання CSRF-токена з cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Знаходимо токен за його ім'ям
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
