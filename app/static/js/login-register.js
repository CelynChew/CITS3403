// Function to toggle password visibility
function PasswordVisibility() {
    var passwordInput = document.getElementById("password");
    var toggleIcon = document.getElementById("showPassword");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleIcon.innerHTML = `<i class="bi bi-eye-fill"></i>`;
    } else {
        passwordInput.type = "password";
        toggleIcon.innerHTML = `<i class="bi bi-eye-slash-fill"></i>`;
    }
}

// Function to redirect to registration page
function createAccount() {
    window.location.href = "registration.html";
}

// Function to check if passwords match during registration
function register() {
    var password = document.getElementById("password").value;
    var retypePassword = document.getElementById("retypePassword").value;
    var errorMessage = document.getElementById("password-match-error");

    if (password !== retypePassword) {
        // Show error message
        errorMessage.style.display = "block";
        console.log("Passwords do not match"); // Add this line for debugging
        return false; // Add this line to prevent form submission
    } else {
        // Hide error message
        errorMessage.style.display = "none";
        return true; // Add this line to allow form submission
    }
}

// Listener for typing animation
document.addEventListener('DOMContentLoaded', function() {
    const text = "Welcome to ChatSome!";
    const element = document.getElementById('welcome-text');
    let index = 0;

    // Create the typing icon element
    const typingIcons = document.createElement('span');
    typingIcons.id = 'typing-icons';
    element.parentNode.insertBefore(typingIcons, element.nextSibling);

    function type() {
        if (index < text.length) {
            element.innerHTML += text.charAt(index);
            index++;
            setTimeout(type, 100);
        } else {
            // Remove the typing icon once typing is done
            typingIcons.style.display = 'none';
            element.style.borderRight = 'none'; // Stop the cursor after typing
        }
    }

    type();
});
