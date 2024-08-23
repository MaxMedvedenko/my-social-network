document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-form').forEach(form => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();

            const postId = form.getAttribute('data-post-id');
            const button = form.querySelector('button');
            const isLike = button.classList.contains('like-btn');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/toggle_like/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams({'is_like': isLike})
            })
            .then(response => response.json())
            .then(data => {
                if (data.likes_count !== undefined) {
                    // Оновлюємо кількість лайків
                    document.querySelector(`#like-count-${postId}`).textContent = `${data.likes_count} Likes`;

                    // Зміна кнопки лайка
                    const likeImg = button.querySelector('img');

                    if (isLike) {
                        button.classList.remove('like-btn');
                        button.classList.add('unlike-btn');
                        likeImg.src = '/static/image/full-heart.svg';
                    } else {
                        button.classList.remove('unlike-btn');
                        button.classList.add('like-btn');
                        likeImg.src = '/static/image/heart.svg';
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
