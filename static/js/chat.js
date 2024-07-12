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

