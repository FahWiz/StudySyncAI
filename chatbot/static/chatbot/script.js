document.addEventListener("DOMContentLoaded", function () {
    // Auto Greet when Page Loads
    let chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<p class="bot"><strong>🤖 StudySync AI:</strong> Hello! Ask me anything.</p>`;
});

// Function to send a message
function sendMessage() {
    let userInput = document.getElementById("user-input").value.trim();
    if (userInput === "") return;

    let chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<p class="user"><strong>You:</strong> ${userInput}</p>`;

    document.getElementById("user-input").value = "";

    function getCSRFToken() {
        let csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return csrfToken ? csrfToken.split('=')[1] : '';
    }
    
    fetch("/api/chatbot/", {  
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()  // Include CSRF token
        },
        body: JSON.stringify({ query: userInput })  
    })
    
    .then(response => response.json())
    .then(data => {
        if (data.response) {
            chatbox.innerHTML += `<p><strong>🤖 StudySync AI:</strong> ${data.response}</p>`;
            if (data.search_url) {
                chatbox.innerHTML += `<p><strong>🤖 StudySync AI:</strong> I couldn't find an answer. Try searching <a href="${data.search_url}" target="_blank">here</a>.</p>`;
            }
        } else {
            chatbox.innerHTML += `<p><strong>🤖 StudySync AI:</strong> Error: No response received</p>`;
        }
        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
        chatbox.innerHTML += `<p><strong>🤖 StudySync AI:</strong> Error: Unable to connect</p>`;
    });
}

// Event Listener for Enter Key
document.getElementById("user-input").addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();  // Prevents line break
        sendMessage();
    }
});
