// Handling chat functionality
function sendMessage() {
    var messageInput = document.getElementById('message-input');
    var message = messageInput.value.trim();   // To remove extra whitespaces that users type before or after the message
    if (message !== '') {
        // To add send message functionality 
        console.log('Message sent:', message);  // For checking
        messageInput.value = ''; // Clear input field after sending message
    }
}

// Allow group name to change 
var groupName = "Person / Group Name"; // Change this to fetch the group name dynamically
document.getElementById('group-name').textContent = groupName;

// Chat examples
var mockChats = ["Chat 1", "Chat 2", "Chat 3"];

// Display mock chats in the chat list
var chatList = document.getElementById('chat-list');
mockChats.forEach(function(chat) {
    var li = document.createElement('li');
    li.textContent = chat;
    li.classList.add('chat'); // Add class for styling
    li.addEventListener('click', function() {
        // Handle chat click event if needed
    });
    chatList.appendChild(li);
});