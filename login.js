function handleLogin(event) {
    event.preventDefault();

    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var errorMessage = document.getElementById('error-message');

    // Check if the entered username and password match the expected values
    if (username === /*username*/ && password === /*password*/) {
        // Authentication successful, redirect to pbl.html
        window.location.href = 'http://127.0.0.1:5000';
    } else {
        // Display an error message for invalid credentials
        errorMessage.textContent = 'Invalid credentials. Please try again.';
    }
}

function togglePasswordVisibility() {
    var passwordInput = document.getElementById('password');
    var showPasswordCheckbox = document.getElementById('showPassword'); // Corrected ID

    passwordInput.type = showPasswordCheckbox.checked ? 'text' : 'password';
}
