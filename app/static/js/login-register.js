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