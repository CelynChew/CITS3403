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

// Function to check if the screen size is small (e.g., mobile)
function isMobile() {
    return window.innerWidth <= 768; // Adjust this threshold as needed
}

// Function to switch between desktop and mobile content
function switchContent() {
    if (isMobile()) {
        document.getElementById('content').style.display = 'none';
        document.getElementById('mobile-content').style.display = 'block';
    } else {
        document.getElementById('content').style.display = 'block';
        document.getElementById('mobile-content').style.display = 'none';
    }
}

// Call the switchContent function initially and on window resize
switchContent();
window.addEventListener('resize', switchContent);