// ===============================
// SHOW / HIDE PASSWORD
// ===============================

const togglePassword = document.getElementById("togglePassword");
const password = document.getElementById("password");

if (togglePassword) {

    togglePassword.addEventListener("click", function () {

        if (password.type === "password") {

            password.type = "text";

            this.classList.remove("fa-eye");
            this.classList.add("fa-eye-slash");

        } else {

            password.type = "password";

            this.classList.remove("fa-eye-slash");
            this.classList.add("fa-eye");

        }

    });

}


// ===============================
// LOGIN
// ===============================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function (e) {

        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        const user = JSON.parse(localStorage.getItem("user"));

        if (!user) {

            alert("No account found. Please register first.");
            return;

        }

        if (email === user.email && password === user.password) {

    localStorage.setItem("loggedIn", "true");

    // Save logged-in user's details
    localStorage.setItem("loggedInUser", JSON.stringify({
        name: user.name,
        email: user.email
    }));

    // alert("Login Successful!");

    window.location.href = "index.html#classify";


        } else {

            alert("Invalid Email or Password.");

        }

    });

}

// ===============================
// REGISTER
// ===============================

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", function (e) {

        e.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        const user = {

            name,
            email,
            password

        };

        localStorage.setItem("user", JSON.stringify(user));

        // alert("Registration Successful!");

        window.location.href = "login.html";

    });

}

// ===============================
// FORGOT PASSWORD
// ===============================

const forgotForm = document.getElementById("forgotForm");

if (forgotForm) {

    forgotForm.addEventListener("submit", function (e) {

        e.preventDefault();

        const email = document.getElementById("forgotEmail").value.trim();

        const user = JSON.parse(localStorage.getItem("user"));

        if (user && user.email === email) {

            alert("Your password is: " + user.password);

        } else {

            alert("Email not found.");

        }

    });

}

