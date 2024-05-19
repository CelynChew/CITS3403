// Establish flask-socketio connection
document.addEventListener('DOMContentLoaded', () => {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        socket.send("I am connected");
    });

    // Display incoming message
    socket.on('message', data => {
        const chatMessagesDiv = document.getElementById('chat-messages');
        const messageElement = document.createElement('p');
        const formattedMessage = data.msg; // Extract the formatted message
        messageElement.textContent = formattedMessage; // Set the text content to the formatted message
        chatMessagesDiv.appendChild(messageElement);
        // Scroll to the bottom of the chat messages div to show the latest messages
        chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;
    });

    // Function to get the username from the HTML
    function getUsername() {
        // Find the element that displays the username
        const usernameElement = document.querySelector('.navbar-brand');
        if (usernameElement) {
            // Extract the username from the element's text content
            return usernameElement.textContent.trim().split(', ')[1];
        }
        return null;
    }

    // Set the global username variable
    let username = getUsername();

    // Send message 
    document.querySelector('#send-button').onclick = () => {
        var messageInput = document.querySelector('#message-input');
        var messageContent = messageInput.value.trim();
        //socket.send({'msg': document.querySelector('#message-input').value, 'username': username});
        if (messageContent !== '') {
            var currentChatName = document.getElementById('group-name').textContent.trim();
            var chatName = currentChatName; // Get the current chat name
            socket.emit('message', {'msg': messageContent, 'username': username, 'chatName': chatName});
            messageInput.value = ''; // Clear the message input field
        }
    }

    // Trigger send button on enter
    var input = document.getElementById('message-input')
    // Event listener for when user presses enter
    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            // Cancel the default action, if needed
            event.preventDefault();
            // Simulate a click on the send button
            document.querySelector('#send-button').click();
        }
    });

    // Socket.IO event listener for file upload
    socket.on('file-upload', function(data) {
        // Update UI to display that a file has been uploaded
        console.log('File uploaded:', data.file_name);
        // You can update UI elements here to notify the user about the uploaded file
        const chatMessagesDiv = document.getElementById('chat-messages');
        const fileElement = document.createElement('p');

        // Create a download link for the uploaded file
        const downloadLink = document.createElement('a');
        downloadLink.href = data.download_link;
        downloadLink.textContent = `Download ${data.file_name}`;
        downloadLink.download = data.file_name;
    
        // Format the message
        const formattedMessage = `${data.username}: ${downloadLink.outerHTML} (${data.timestamp})`;
        fileElement.innerHTML = formattedMessage;
        chatMessagesDiv.appendChild(fileElement);

        // Scroll to the bottom of the chat messages div to show the latest messages
        chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;
    });

})

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
                // Check if file_name field is null to decide which content to append into chat display area
                let content;
                if (message.file_name !== null) {
                    // Creating a download link for files
                    const fileName = message.file_name;
                    content = `<a href="/uploads/${fileName}" download="${fileName}">Download ${fileName}</a>`;
                } else {
                    content = message.message; // Display message text
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
                // File uploaded successfully
                // Fetch chat ID based on chat name
                fetch(`/get_chat_id/${chatName}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        // Call updateChatDisplay with the retrieved chat ID and chat name
                        updateChatDisplay(data.chatId, chatName);
                    })
                    .catch(error => console.error('Error fetching chat ID:', error));
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

    // Exit the function if member field is empty
    if (members === "") {
        console.log("Members field is empty. Cannot create new chat.");
        return;
    }

    var chatName = members;

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

        location.reload();
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
// Get message input, upload button, and send button elements
var messageInput = document.getElementById('message-input');
var uploadButton = document.getElementById('uploadFile');
var sendButton = document.getElementById('send-button');

// Function to enable message input, upload button, and send button
function enableInputs() {
    messageInput.disabled = false;
    uploadButton.disabled = false;
    sendButton.disabled = false;
}

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
        // Enable message input, upload and send buttons
        enableInputs();
    } else {
        // Otherwise, disable the inputs
        messageInput.disabled = true;
        uploadButton.disabled = true;
        sendButton.disabled = true;
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
    if (window.innerWidth <= 1000) {
    window.location.href = "/tutorial-m"; }
    else {
        window.location.href = "/tutorial";
    }
}

// Listener to switch content on screen resizing
window.addEventListener('resize', switchContent);

// Functions to open and close sidenav bar
function openNav() {
    document.getElementById("chats").style.width = "250px";
}

function closeNav() {
    document.getElementById("chats").style.width = "0";
}

// Function to check if the screen size is small 
function isMobile() {
    return window.innerWidth <= 900; 
}

let isMobileScreen = isMobile(); // Store initial screen size state
console.log(isMobileScreen)

// Function to check window width and redirect accordingly
function switchContent() {
    const currentIsMobile = isMobile(); // Get current screen size
    if (currentIsMobile !== isMobileScreen) { // Check if there's a change in screen size
        isMobileScreen = currentIsMobile; // Update the stored screen size state
        if (isMobileScreen) { 
            window.location.href = "/chatroom-m"; // Redirect to mobile chatroom route
        } else {
            window.location.href = "/chatroom"; // Redirect to default chatroom route
        }
    }
}

