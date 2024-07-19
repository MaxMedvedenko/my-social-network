function scrollToBottom() {
    var messagesContainer = document.getElementById("messages");
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function() {
    scrollToBottom();
});

function addMessage(content) {
    var messagesContainer = document.getElementById("messages");
    var newMessageDiv = document.createElement("div");
    newMessageDiv.classList.add("message");
    newMessageDiv.innerHTML = `<strong>${content.sender}</strong>: ${content.message} <span class="timestamp">${content.timestamp}</span>`;
    
    messagesContainer.appendChild(newMessageDiv);
    scrollToBottom();
}

//--- for edit message ---//

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('edit-message-link')) {
            e.preventDefault();
            const messageId = e.target.getAttribute('data-message-id');
            const messageElement = document.querySelector(`.message[data-message-id="${messageId}"]`);
            const messageContentElement = messageElement.querySelector('.message-content');

            if (messageElement.classList.contains('editing')) {
                return;
            }

            const originalContent = messageContentElement.textContent.trim();

            // Create and display the edit form
            const editMessageForm = document.createElement('form');
            editMessageForm.classList.add('edit-message-form');
            editMessageForm.setAttribute('id', `edit-message-form-${messageId}`);
            
            const textarea = document.createElement('textarea');
            textarea.classList.add('message-textarea');
            textarea.setAttribute('name', 'content');
            textarea.setAttribute('rows', '4');
            textarea.style.width = '100%';
            textarea.style.padding = '10px';
            textarea.style.border = '1px solid #ddd';
            textarea.style.borderRadius = '5px';
            textarea.style.marginBottom = '10px';
            textarea.style.maxWidth = '1000px';
            textarea.textContent = originalContent;

            editMessageForm.appendChild(textarea);

            const saveButton = document.createElement('button');
            saveButton.setAttribute('type', 'submit');
            saveButton.classList.add('edit-message-btn');
            saveButton.textContent = 'Save';

            editMessageForm.appendChild(saveButton);

            messageContentElement.innerHTML = '';
            messageContentElement.appendChild(editMessageForm);

            // Handle form submission
            editMessageForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const formData = new FormData(this);

                fetch(`/messages/${messageId}/edit/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        messageContentElement.textContent = formData.get('content');
                        messageElement.classList.remove('editing');
                    } else {
                        console.error('Error updating message:', data.error);
                    }
                })
                .catch(error => console.error('Error updating message:', error));
            });

            messageElement.classList.add('editing');
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
