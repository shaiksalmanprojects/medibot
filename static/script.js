document.addEventListener("DOMContentLoaded", function() {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");

    function addMessage(message, isUser = false) {
        const messageElement = document.createElement("div");
        messageElement.classList.add(isUser ? "user-message" : "bot-message");
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === "") return;

        addMessage(userMessage, true);
        userInput.value = "";

        fetch("/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_input: userMessage }),
        })
            .then((response) => response.json())
            .then((data) => {
                const botResponse = data.response;
                const medicine = data.medicine;
                addMessage(botResponse);
                if (medicine) {
                    addMessage(`Recommended Medicine: ${medicine}`);
                }
            })
            .catch((error) => {
                console.error("Error sending message:", error);
            });
    }

    sendButton.addEventListener("click", sendMessage);

    userInput.addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});