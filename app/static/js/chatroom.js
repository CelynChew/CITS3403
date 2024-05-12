// Function to fetch messages and update the chat display
function updateChatDisplay(chatId, chatName) {
    fetch(`/get_messages/${chatId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const chatMessagesDiv = document.getElementById('chat-messages');
            // Clear existing messages
            chatMessagesDiv.innerHTML = '';
            // Loop through the messages and append them to the chat messages div
            data.forEach(message => {
                const messageElement = document.createElement('p');
                // Check if msg_text field is null to decide which content to append into chat display area
                let content;
                if (message.message !== null) {
                    content = message.message;
                } else {
                    // Creating a download link
                    // Extract filename from the file path by getting last element of array
                    const fileName = message.file_path.split('/').pop();
                    content = `<a href="${message.file_path}" download="${fileName}">Download ${fileName}</a>`;
                }
                messageElement.innerHTML = `${message.sender_username}: ${content} (${message.timestamp})`;
                chatMessagesDiv.appendChild(messageElement);
            });
            // Scroll to the bottom of the chat messages div to show the latest messages
            chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;

            // Display the chat name
            document.getElementById('group-name').textContent = chatName;
        })
        .catch(error => console.error('Error fetching messages:', error));
}

// Call the updateChatDisplay function when the page loads
window.addEventListener('load', updateChatDisplay);

var chatList = document.getElementById('chat-list');
// Listener for displaying messages
chatList.addEventListener('click', function(event) {
    var clickedElement = event.target;
    
    // Finding chat list items
    while (clickedElement && clickedElement.tagName !== 'LI') {
        clickedElement = clickedElement.parentElement;
    }
    
    // Display messages for each chat
    if (clickedElement && clickedElement.classList.contains('chat')) {
        var chatId = clickedElement.dataset.chatId;
        var chatName = clickedElement.textContent.trim();
        
        updateChatDisplay(chatId, chatName); 
    }
});

// Function to open file input page
function openFileInput() {
    document.getElementById('fileInput').click();
}

function sendFileToFlask(event, chatName) {
    const file = event.target.files[0]; // Getting the file

    // Sending file to Flask
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('chat_name', chatName); // Append chat name to the FormData

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // For checking
                console.log('File uploaded successfully');
            } else {
                console.error('File upload failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

var fileInput = document.getElementById('fileInput');
fileInput.addEventListener("change", function(event) {
    // Retrieve selected chat name
    var currentChatName = document.getElementById('group-name').textContent.trim();
    // Pass both event and chat name to sendFileToFlask
    sendFileToFlask(event, currentChatName);
});

// Function to send a message
function sendMessage(chatName) {
    // Get the message input element
    var messageInput = document.getElementById('message-input');
    // Get the trimmed message content
    var messageContent = messageInput.value.trim();

    // Check if the message is not empty
    if (messageContent !== '') {
        // Fetch the chatId based on chatName
        fetch(`/get_chat_id/${chatName}`)
        .then(response => {
            // Check if the response is successful
            if (!response.ok) {
                throw new Error('Failed to fetch chatId');
            }
            // Parse the response JSON data
            return response.json();
        })
        .then(data => {
            // Once chatId is obtained, send the message
            var chatId = data.chatId;
            // Send the message to the backend
            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: messageContent, chat_id: chatId, chat_name: chatName })
            })
            .then(response => {
                // Check if the response is successful
                if (!response.ok) {
                    throw new Error('Failed to send message');
                }
                // Parse the response JSON data
                return response.json();
            })
            .then(data => {
                // Log a success message
                console.log('Message sent successfully:', data.message);
                // Clear the message input field
                messageInput.value = '';
                // Update the chat display to show the new message
                updateChatDisplay(chatId, chatName);
            })
            .catch(error => {
                // Log any errors that occurred during message sending
                console.error('Failed to send message:', error);
            });
        })
        .catch(error => {
            // Log any errors that occurred during chatId fetching
            console.error('Failed to fetch chatId:', error);
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
        // Retrieve selected chat name
        var currentChatName = document.getElementById('group-name').textContent.trim();
        sendMessage(currentChatName); // Call the sendMessage function when Enter is pressed
    }
});
var sendButton = document.getElementById('send-button')
sendButton.addEventListener("click", function(event) {
    // Retrieve selected chat name
    var currentChatName = document.getElementById('group-name').textContent.trim();
    sendMessage(currentChatName); // Send Message
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
    fetch(`/create_chat`, {
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
        // Clear alert messages
        document.getElementById('chat-alert-container').innerHTML = '';
        document.getElementById('user-alert-container').innerHTML = '';

        // Display chat in the chat list
        fetchChats();

        // Check for chat_alert and user_alert messages
        if (data.chat_alert) {
            // Alert for replicated chats
            document.getElementById('chat-alert-container').innerHTML = '<div class="alert alert-danger">' + data.chat_alert + '</div>';
            
        } else if(data.user_alert) {
            // Alert for non-exisiting users
            document.getElementById('user-alert-container').innerHTML = '<div class="alert alert-danger">' + data.user_alert + '</div>';
            
        } else {
            // Close modal after chat is created
            newChatModal.classList.remove('show');
            document.querySelector('.modal-backdrop').remove()
        }
    })
    .catch(error => {
        console.error('There was a problem creating the chat:', error);
    });

    // Clear input fields
    membersInput.value = "";
    groupNameInput.value = "";
}

// Function to delete a chat
function deleteChat(chatId, chatListItem) {
    // Send a DELETE request to the Flask backend to delete the chat
    fetch(`/chats`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ chat_id: chatId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Remove chat item from the chat list
        chatListItem.remove();
    })
    .catch(error => {
        console.error('There was a problem deleting the chat:', error);
    });
}

// Function to fetch existing chats
function fetchChats() {
    // GET request to the Flask backend to display existing chats
    fetch(`/chats`)
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
            chatListItem.dataset.chatId = chat.chat_id; // Add chat_id as data attribute

            chatListItem.classList.add('chat'); // Adding .chat CSS to the chatListItem

            // Create delete button/icon
            var deleteButton = document.createElement('button');
            deleteButton.classList.add('delete-group-btn', 'btn', 'btn-danger', 'btn-sm'); // Adding Bootstrap button classes
            deleteButton.innerHTML = '<i class="bi bi-trash"></i>';

            // Append the delete button to the chat list item
            chatListItem.appendChild(deleteButton);

            // Add event listener for delete button/icon
            deleteButton.addEventListener('click', function(event) {
                event.stopPropagation();
                // Calling deleteChat() to delete selected chat
                deleteChat(chat.chat_id, chatListItem);
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
        var groupName = clickedElement.textContent.trim();
        
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
    fetch('/logout', {
        method: 'GET',
        credentials: 'same-origin' // Include cookies in the request
    })
    .then(response => {
        // Handle successful logout
        window.location.href = "/";
    })
    .catch(error => {
        // Handle errors
        console.error('Logout error:', error);
    });
}

// Function for going to tutotial page
function showTutorial() {
    window.location.href = "/tutorial"; 
}
