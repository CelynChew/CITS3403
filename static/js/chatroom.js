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

// Search bar functionality 
document.getElementById('search-chat').addEventListener('input', function() {
    var searchVal = this.value.trim().toLowerCase(); // clean the search value - remove white spaces + change all to lower case
    var chatList = document.querySelectorAll('#chat-list li'); // select all chat in chat list

    // Loop through the chat list
    chatList.forEach(function(item) {
        var itemName = item.textContent.trim().toLowerCase(); // clean chat list names 
        // If the chat item matches the search term, show it; otherwise, hide it - remove white spaces + change all to lower case
        if (itemName.includes(searchVal)) { // allow for flexibl search 
            item.style.display = 'block';
        } else {
            item.style.display = 'none'; // hiding chats that are not searched for
        }
    });
});
