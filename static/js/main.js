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


//--- for add comment ---//

document.addEventListener('DOMContentLoaded', function() {
    // Обробка подій для форми додавання коментаря
    const addCommentForm = document.getElementById('add-comment-form');
    addCommentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch(`/post/${addCommentForm.dataset.postId}/add_comment/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Додати новий коментар до секції коментарів
                const commentsSection = document.querySelector('.comments');
                const newComment = document.createElement('div');
                newComment.classList.add('comment');
                newComment.setAttribute('id', `comment-${data.comment.id}`);
                newComment.innerHTML = `
                    <p class="comment-meta">Comment by ${data.comment.user} on ${data.comment.created_at}</p>
                    <p class="comment-content">${data.comment.content}</p>
                    <div class="comment-actions">
                        <a href="#" class="edit-comment-link" data-comment-id="${data.comment.id}">Edit</a>
                        <form method="post" action="/delete_comment/${data.comment.id}/">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
                            <button type="submit" class="delete-comment-btn">Delete</button>
                        </form>
                    </div>
                `;
                commentsSection.appendChild(newComment);

                // Очистити поле вводу коментаря після успішного додавання
                document.getElementById('comment-content').value = '';
            } else {
                console.error('Error adding comment:', data.error);
            }
        })
        .catch(error => console.error('Error adding comment:', error));
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});



//--- for edit comment ---//

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('edit-comment-link')) {
            e.preventDefault();
            const commentId = e.target.getAttribute('data-comment-id');
            const commentElement = document.getElementById(`comment-${commentId}`);
            const commentContentElement = commentElement.querySelector('.comment-content');

            if (commentElement.classList.contains('editing')) {
                return;
            }

            commentElement.classList.add('editing');
            const originalContent = commentContentElement.textContent.trim();

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
            textarea.style.maxWidth = '1000px';
            textarea.value = originalContent;

            editCommentForm.appendChild(textarea);

            const saveButton = document.createElement('button');
            saveButton.setAttribute('type', 'submit');
            saveButton.classList.add('edit-comment-btn');
            saveButton.textContent = 'Save';

            editCommentForm.appendChild(saveButton);

            commentContentElement.innerHTML = '';
            commentContentElement.appendChild(editCommentForm);

            editCommentForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);

                fetch(`/comment/${commentId}/edit/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        commentContentElement.textContent = formData.get('content');
                        commentElement.classList.remove('editing');
                    } else {
                        console.error('Error updating comment:', data.error);
                    }
                })
                .catch(error => console.error('Error updating comment:', error));
            });
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
