// Function to fetch messages and update the chat display
function updateChatDisplay() {
    fetch('/get_messages')
        .then(response => response.json())
        .then(data => {
            const chatMessagesDiv = document.getElementById('chat-messages');
            // Clear existing messages
            chatMessagesDiv.innerHTML = '';
            // Loop through the messages and append them to the chat messages div
            data.forEach(message => {
                const messageElement = document.createElement('p');
                messageElement.textContent = `${message.user_id}: ${message.message} (${message.timestamp})`;
                chatMessagesDiv.appendChild(messageElement);
            });
            // Scroll to the bottom of the chat messages div to show the latest messages
            chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;
        })
        .catch(error => console.error('Error fetching messages:', error));
}

// Call the updateChatDisplay function when the page loads
window.addEventListener('load', updateChatDisplay);

// Function to send a message
function sendMessage() {
    var messageInput = document.getElementById('message-input');
    var message = messageInput.value.trim();
    if (message !== '') {
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Message sent:', data.message);
            // After successfully sending message, clear input field
            messageInput.value = '';
            // Update the chat display to show the new message
            updateChatDisplay();
        })
        .catch(error => {
            console.error('There was a problem with sending your message:', error);
        });
    }
}

// Trigger send button on enter
var input = document.getElementById('message-input')
// Event listener for when user presses enter
input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        // Cancel the default action, if needed
        event.preventDefault();
        sendMessage(); // Call the sendMessage function when Enter is pressed
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

    var chatName;
    // Construct the chat item string based on whether a group name is provided
    if (groupName !== "") {
        chatName = groupName; // Use group name only
    } else {
        chatName = members; // Use members only
    }

    // Send a POST request to the Flask backend to create chat
    fetch('/create_chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ chat_name: chatName })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Chat created:', data.message);
        // If chat creation is successful, chat will be displayed
        fetchChats();
    })
    .catch(error => {
        console.error('There was a problem creating the chat:', error);
    });

    // Clear input fields
    membersInput.value = "";
    groupNameInput.value = "";

    // Close modal after chat is created
    newChatModal.classList.remove('show');
    document.querySelector('.modal-backdrop').remove() // Remove modal backdrop
}

// Function to fetch existing chats
function fetchChats() {
    // GET request to the Flask backend to display existing chats
    fetch('/chats')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Clear the existing chat list
        chatList.innerHTML = '';
        
        // Loop through fetched chat and add to the chat list
        data.chats.forEach(chat => {
            // Create a new list item for the chat
            var chatListItem = document.createElement('li');
            chatListItem.textContent = chat.chat_name;

            chatListItem.classList.add('chat'); // Adding .chat CSS to the chatListItem

            // Create delete button/icon
            var deleteButton = document.createElement('button');
            deleteButton.classList.add('delete-group-btn', 'btn', 'btn-danger', 'btn-sm'); // Adding Bootstrap button classes
            deleteButton.textContent = 'x';

            // Append the delete button to the chat list item
            chatListItem.appendChild(deleteButton);

            // Add event listener for delete button/icon
            deleteButton.addEventListener('click', function(event) {
                event.stopPropagation();
                chatListItem.remove(); // Remove the chat item from the chat list
            });

            // Add the new chat item to the chat list
            chatList.appendChild(chatListItem);
        });
    })
    .catch(error => {
        console.error('There was a problem fetching chats:', error);
    });
}

// Call fetchChats() when the page loads
fetchChats();

// Function to clear input fields when modal is closed
function clearFields() {
    membersInput.value = ""; // Clear members input field
    groupNameInput.value = ""; // Clear group name input field
}

// Get the group name element
var groupNameElement = document.getElementById('group-name');

// Listener for updating chat display header
chatList.addEventListener('click', function(event) {
    // Setting variable name for element that was clicked
    var clickedElement = event.target;
    
    // Finding chat items
    while (clickedElement && clickedElement.tagName !== 'LI') {
        clickedElement = clickedElement.parentElement;
    }
    
    // If a chat item was clicked, the chat name will be updated
    if (clickedElement && clickedElement.classList.contains('chat')) {
        var clickedText = clickedElement.textContent.trim();
        
        // Exclude the last character (which is 'x')
        var groupName = clickedText.substring(0, clickedText.length - 1);
        
        // Updating the displayed chat name
        groupNameElement.textContent = groupName;
    }
});

// Search bar functionality 
document.getElementById('search-chat').addEventListener('input', function() {
    var searchVal = this.value.trim().toLowerCase(); // clean the search value - remove white spaces + change all to lower case
    var chatList = document.querySelectorAll('#chat-list li'); // select all chat in chat list

    // Loop through the chat list
    chatList.forEach(function(item) {
        var itemName = item.textContent.trim().toLowerCase(); // clean chat list names 
        
        // Exclude the last character ('x')
        if (itemName.charAt(itemName.length - 1) === 'x') {
            itemName = itemName.substring(0, itemName.length - 1);
        }
        
        // If the chat item matches the search term, show it; otherwise, hide it - remove white spaces + change all to lower case
        if (itemName.includes(searchVal)) { // allow for flexible search 
            item.style.display = 'block';
        } else {
            item.style.display = 'none'; // hiding chats that are not searched for
        }
    });
});

// Function for logging out
function LoggingOut() {
    window.location.href = "/";
}
