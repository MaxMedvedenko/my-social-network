// Function to scroll the messages container to the bottom
function scrollToBottom() {
    var messagesContainer = document.getElementById("messages");
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Event listener for DOMContentLoaded to scroll on page load
document.addEventListener("DOMContentLoaded", function() {
    scrollToBottom();
});

// Function to add a new message to the DOM
function addMessage(content) {
    var messagesContainer = document.getElementById("messages");
    var newMessageDiv = document.createElement("div");
    newMessageDiv.classList.add("message");
    newMessageDiv.innerHTML = `<strong>${content.sender}</strong>: ${content.message} <span class="timestamp">${content.timestamp}</span>`;
    
    messagesContainer.appendChild(newMessageDiv);
    scrollToBottom();
}

