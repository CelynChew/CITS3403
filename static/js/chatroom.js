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

// Trigger send button on enter
var input = document.getElementById('message-input')
// Event listener for when user presses enter
input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        // Cancel the default action, if needed
        event.preventDefault();
        document.getElementById("send-button").click();
    }
});

// Function to add new chats to chat list 
var chatList = document.getElementById('chat-list');
var createChatForm = document.getElementById('create-chat-form');
var membersInput = document.getElementById('members-input');
var groupNameInput = document.getElementById('group-name-input');
var newChatModal = document.getElementById('new-chat-form');

function createChat() {
    // Get values from input fields and remove extra white spaces
    var members = membersInput.value.trim();
    var groupName = groupNameInput.value.trim();

    // Exit the function if member field is empty
    if (members === "") {
        console.log("Members field is empty. Cannot create new chat.");
        return; 
    }    

    // Create a new list item
    var chatListItem = document.createElement('li');

    // Construct the chat item string based on whether a group name is provided
    if (groupName !== "") {
        chatListItem.textContent = groupName; // Use group name only
    } else {
        chatListItem.textContent = members; // Use members only
    }

    chatListItem.classList.add('chat'); // Adding .chat CSS to the chatListItem
    console.log("New chat created:", chatListItem);

    // Add the new chat item to the chat list
    chatList.appendChild(chatListItem);

    // Clear input fields
    membersInput.value = "";
    groupNameInput.value = "";

    // Close modal after chat is created
    newChatModal.classList.remove('show');
}

// Function to clear input fields when modal is closed
function clearFields() {
    membersInput.value = ""; // Clear members input field
    groupNameInput.value = ""; // Clear group name input field
}

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
