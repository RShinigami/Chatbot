document.getElementById('send-button').addEventListener('click', sendMessage);
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const loader = document.getElementById('loader');
const message = userInput.value;

async function sendMessage() {
    const userInputValue = userInput.value.trim();
    if (userInputValue !== '') {
        appendMessage(userInputValue, 'You');
        userInput.value = '';
        sendButton.classList.remove('active');

        // Show loader and disable input field
        const loader = document.getElementById('loader');
        loader.style.display = 'block';
        userInput.classList.add('loading');
        userInput.disabled = true;

        try {
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userInputValue })
            });
            
            const data = await response.json();
            if (response.ok) {
                appendMessage(data.response, 'bot');
            } else {
                console.error('Error:', data);
                appendMessage('Sorry, there was an error processing your message.', 'bot');
            }
        } catch (error) {
            console.error('Error:', error);
            appendMessage('Sorry, there was an error connecting to the server.', 'bot');
        } finally {
            // Hide loader and enable input field
            loader.style.display = 'none';
            userInput.classList.remove('loading');
            userInput.disabled = false;
            userInput.focus();
        }
    }
}

document.getElementById('logout-button').addEventListener('click', function() {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
    })
    .catch(error => console.error('Error:', error));
});



document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        sendMessage();
    }
});

function appendMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    if (sender === 'You') {
        messageElement.classList.add('user-message');
    } else {
        messageElement.classList.add('bot-message');
    }

    const senderLabel = document.createElement('div');
    senderLabel.classList.add('message-sender');
    senderLabel.innerText = sender === 'You' ? 'You' : 'Chatbot';
    messageElement.appendChild(senderLabel);

    const messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.innerText = message;
    messageElement.appendChild(messageContent);

    document.getElementById('chat-messages').appendChild(messageElement);
    document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
}

userInput.addEventListener('input', function() {
    if (this.value.trim() !== '') {
        sendButton.classList.add('active');
    } else {
        sendButton.classList.remove('active');
    }
});

const modeSwitchBtn = document.getElementById('mode-switch-btn');
const sidebar = document.getElementById('sidebar');

modeSwitchBtn.addEventListener('click', toggleMode);

function toggleMode() {
    document.body.classList.toggle('dark-mode');
    sidebar.classList.toggle('dark-mode');
    logoutButton.classList.toggle('dark-mode');
    const icon = modeSwitchBtn.querySelector('i');
    if (document.body.classList.contains('dark-mode')) {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
    } else {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
    }
}

const sidebarToggle = document.getElementById('sidebar-toggle');
const username = document.getElementById('username');
const logoutButton = document.getElementById('logout-button');
const chatContainer = document.querySelector('.chat-container');
const chatMessages = document.querySelector('.chat-messages');

sidebarToggle.addEventListener('click', function() {
    sidebar.classList.toggle('sidebar-open');
    chatMessages.classList.toggle('sidebar-open');
    if (sidebar.classList.contains('sidebar-open')) {
        username.style.display = 'block';
        logoutButton.innerHTML = 'Logout';
        sidebar.style.width = '180px';
        chatMessages.style.paddingLeft = '200px';
        sidebarToggle.innerHTML = '<i class="fas fa-times"></i>';
    } else {
        username.style.display = 'none';
        logoutButton.innerHTML = '<i class="fas fa-sign-out-alt"></i>';
        sidebar.style.width = '50px';
        chatMessages.style.paddingLeft = '60px';
        sidebarToggle.innerHTML = '<i class="fas fa-bars"></i>';
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const defaultMessage = "Hello, how can I help you today!";
    appendMessage(defaultMessage, 'bot');
});

document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const loader = document.getElementById('loader');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const logoutButton = document.getElementById('logout-button');
    const databaseChatButton = document.getElementById('database-chat-button');
    const mainChatButton = document.getElementById('main-chat-button');
    const modeSwitchButton = document.getElementById('mode-switch-btn');
    let darkMode = false;

    const handleSendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'user-message');
        messageElement.innerHTML = `<div class="message-content">${message}</div>`;
        chatMessages.appendChild(messageElement);
        userInput.value = '';

        loader.style.display = 'block';

        try {
            const response = await fetch(window.location.pathname, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            const botMessage = data.response;

            const botMessageElement = document.createElement('div');
            botMessageElement.classList.add('message', 'bot-message');
            botMessageElement.innerHTML = `<div class="message-content">${botMessage}</div>`;
            chatMessages.appendChild(botMessageElement);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            loader.style.display = 'none';
        }
    };

    const toggleSidebar = () => {
        sidebar.classList.toggle('active');
    };

    const switchMode = () => {
        darkMode = !darkMode;
        if (darkMode) {
            document.body.classList.add('dark-mode');
            modeSwitchButton.innerHTML = '<i class="fas fa-moon"></i>';
        } else {
            document.body.classList.remove('dark-mode');
            modeSwitchButton.innerHTML = '<i class="fas fa-sun"></i>';
        }
    };

    sendButton.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            handleSendMessage();
        }
    });

    sidebarToggle.addEventListener('click', toggleSidebar);
    logoutButton.addEventListener('click', () => {
        window.location.href = '/logout';
    });

    if (databaseChatButton) {
        databaseChatButton.addEventListener('click', () => {
            window.location.href = '/database_chat';
        });
    }

    if (mainChatButton) {
        mainChatButton.addEventListener('click', () => {
            window.location.href = '/chat';
        });
    }

    modeSwitchButton.addEventListener('click', switchMode);
});

