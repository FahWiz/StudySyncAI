// Toggle between Login & Register forms
function toggleForm() {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const formTitle = document.getElementById("form-title");

    if (loginForm.style.display === "none") {
        loginForm.style.display = "block";
        registerForm.style.display = "none";
        formTitle.textContent = "Login";
    } else {
        loginForm.style.display = "none";
        registerForm.style.display = "block";
        formTitle.textContent = "Register";
    }
}

// Toggle Password Visibility
function togglePassword(inputId) {
    let input = document.getElementById(inputId);
    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}
