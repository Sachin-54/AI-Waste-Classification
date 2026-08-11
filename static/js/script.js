// ===============================
// FILE UPLOAD PREVIEW
// ===============================

const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const preview = document.getElementById("preview");
const predictBtn = document.getElementById("predictBtn");
const resultCard = document.getElementById("resultCard");
const predictionText = document.getElementById("predictionText");
const previewContainer = document.querySelector(".preview-container");
const removeImage = document.getElementById("removeImage");
const uploadContent = document.getElementById("uploadContent");

// ===============================
// HIDE CLASSIFY NAV BEFORE LOGIN
// ===============================

const classifyNav = document.getElementById("classifyNav");

if (classifyNav) {

    const loggedIn = localStorage.getItem("loggedIn");

    if (loggedIn !== "true") {
        classifyNav.style.display = "none";
    }

}

// ===============================
// LOGIN CHECK
// ===============================

document.addEventListener("DOMContentLoaded", () => {

    const uploadSection = document.getElementById("classify");

    if (localStorage.getItem("loggedIn") === "true") {

        uploadSection.classList.remove("hidden-upload");

    } else {

        uploadSection.classList.add("hidden-upload");

    }

});

if (fileInput) {

    fileInput.addEventListener("change", function () {

        if (this.files.length > 0) {

            const file = this.files[0];

            fileName.textContent = file.name;

            const reader = new FileReader();

            reader.onload = function (e) {

                preview.src = e.target.result;

                uploadContent.style.display = "none";
                previewContainer.style.display = "block";

            };

            reader.readAsDataURL(file);

        }

    });

}


// ===============================
// REMOVE / CROSS BUTTON
// ===============================

if (removeImage) {

    removeImage.addEventListener("click", () => {

        fileInput.value = "";
        preview.src = "";

        previewContainer.style.display = "none";
        uploadContent.style.display = "block";

        fileName.textContent = "No file selected";

        resultCard.style.display = "none";
        predictionText.textContent = "-";

    });

}


// ===============================
// PREDICT IMAGE
// ===============================

if (predictBtn) {

    predictBtn.addEventListener("click", async () => {

        // ===============================
        // CHECK LOGIN
        // ===============================

        if (localStorage.getItem("loggedIn") !== "true") {
            alert("Please login first.");
            window.location.href = "login.html";
            return;
        }

        // ===============================
        // CHECK IMAGE
        // ===============================

        if (fileInput.files.length === 0) {
            alert("Please choose an image first.");
            return;
        }

        // ===============================
        // PREPARE IMAGE
        // ===============================

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        // ===============================
        // SHOW LOADING
        // ===============================

        predictBtn.innerHTML = "Predicting...";
        predictBtn.disabled = true;

        try {

            // ===============================
            // SEND IMAGE TO FLASK
            // ===============================

            const response = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                body: formData
            });

            // ===============================
            // GET RESPONSE
            // ===============================

            const data = await response.json();

            console.log("Flask response:", data);

            // ===============================
            // SHOW RESULT
            // ===============================

            resultCard.style.display = "block";

            if (data.success === true) {

                predictionText.innerHTML = data.prediction;

            } else {

                predictionText.innerHTML =
                    "Prediction failed";

                console.error("Backend error:", data.error);
                console.error("Details:", data.details);

                alert(
                    "Prediction failed.\n\n" +
                    (data.error || "Unknown error")
                );
            }

        } catch (error) {

            console.error("Connection error:", error);

            resultCard.style.display = "block";

            predictionText.innerHTML =
                "Server error";

            alert(
                "Unable to connect to Flask server.\n\n" +
                "Make sure app.py is running."
            );

        } finally {

            predictBtn.innerHTML = "Predict Waste Type";
            predictBtn.disabled = false;

        }

    });

}


// ===============================
// CATEGORY POPUP
// ===============================

function showInfo(title, text) {

    document.getElementById("infoTitle").innerHTML = title;

    document.getElementById("infoText").innerHTML = text;

    document.getElementById("modalOverlay").classList.add("active");

    document.getElementById("infoBox").classList.add("active");

}

function closeInfo() {

    document.getElementById("modalOverlay").classList.remove("active");

    document.getElementById("infoBox").classList.remove("active");

}

document.addEventListener("keydown", function (e) {

    if (e.key === "Escape") {

        closeInfo();

    }

});


// ===============================
// ACTIVE NAVBAR
// ===============================

const sections = document.querySelectorAll("section");

const navLinks = document.querySelectorAll("nav ul li a");

window.addEventListener("scroll", () => {

    let current = "";

    sections.forEach(section => {

        const sectionTop = section.offsetTop - 150;

        if (pageYOffset >= sectionTop) {

            current = section.getAttribute("id");

        }

    });

    navLinks.forEach(link => {

        link.classList.remove("active");

        if (link.getAttribute("href") === "#" + current) {

            link.classList.add("active");

        }

    });

});


// ===============================
// FADE ANIMATION
// ===============================

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

        }

    });

});

document.querySelectorAll("section").forEach(section => {

    section.classList.add("hidden");

    observer.observe(section);

});


// ===============================
// SMOOTH SCROLL
// ===============================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        const target = this.getAttribute("href");

        // Check only for Classify button
        if (target === "#classify") {

            e.preventDefault();

            if (localStorage.getItem("loggedIn") === "true") {

                document.querySelector(target).scrollIntoView({
                    behavior: "smooth"
                });

            } else {

                alert("Please login or register to access the Waste Classifier.");

                window.location.href = "login.html";

            }

        } else {

            e.preventDefault();

            document.querySelector(target).scrollIntoView({
                behavior: "smooth"
            });

        }

    });

});

const userBtn = document.getElementById("userBtn");
const userDropdown = document.getElementById("userDropdown");

const guestMenu = document.getElementById("guestMenu");
const profileMenu = document.getElementById("profileMenu");

const user = JSON.parse(localStorage.getItem("loggedInUser"));

if(user){

    guestMenu.style.display="none";
    profileMenu.style.display="block";

    document.getElementById("userName").textContent=user.name;
    document.getElementById("userEmail").textContent=user.email;

}else{

    guestMenu.style.display="block";
    profileMenu.style.display="none";

}

userBtn.addEventListener("click",(e)=>{

    e.stopPropagation();

    userDropdown.classList.toggle("show");

});

document.addEventListener("click",()=>{

    userDropdown.classList.remove("show");

});

document.getElementById("logoutBtn").addEventListener("click",()=>{

    localStorage.removeItem("loggedIn");
    localStorage.removeItem("loggedInUser");

    location.reload();

});


const chooseImageBtn = document.getElementById("chooseImageBtn");

chooseImageBtn.addEventListener("click", function () {

    const loggedIn = localStorage.getItem("loggedIn");

    if (loggedIn === "true") {

        document.getElementById("fileInput").click();

    } else {

        window.location.href = "login.html";

    }

});

const faqItems = document.querySelectorAll(".faq-item");

faqItems.forEach(item=>{

    const question=item.querySelector(".faq-question");

    question.addEventListener("click",()=>{

        faqItems.forEach(faq=>{

            if(faq!==item){

                faq.classList.remove("active");

            }

        });

        item.classList.toggle("active");

    });

});

// ===============================
// DARK MODE
// ===============================

const themeToggle = document.getElementById("themeToggle");

if (themeToggle) {

    const themeIcon = themeToggle.querySelector("i");

    // Load saved theme
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {

        document.body.classList.add("dark-mode");

        themeIcon.classList.remove("fa-moon");
        themeIcon.classList.add("fa-sun");

    }

    themeToggle.addEventListener("click", () => {

        document.body.classList.toggle("dark-mode");

        const darkMode = document.body.classList.contains("dark-mode");

        if (darkMode) {

            localStorage.setItem("theme", "dark");

            themeIcon.classList.remove("fa-moon");
            themeIcon.classList.add("fa-sun");

        } else {

            localStorage.setItem("theme", "light");

            themeIcon.classList.remove("fa-sun");
            themeIcon.classList.add("fa-moon");

        }

    });

}

// ==========================================================
// MOBILE NAVIGATION
// ==========================================================

const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const navbar = document.querySelector("nav");

if (mobileMenuBtn && navbar) {

    mobileMenuBtn.addEventListener("click", function (e) {

        e.stopPropagation();

        navbar.classList.toggle("mobile-open");

        const icon = this.querySelector("i");

        if (navbar.classList.contains("mobile-open")) {

            icon.classList.remove("fa-bars");
            icon.classList.add("fa-xmark");

        } else {

            icon.classList.remove("fa-xmark");
            icon.classList.add("fa-bars");

        }

    });


    // Close menu when clicking a navigation link

    const mobileLinks = navbar.querySelectorAll("ul a");

    mobileLinks.forEach(link => {

        link.addEventListener("click", function () {

            navbar.classList.remove("mobile-open");

            const icon = mobileMenuBtn.querySelector("i");

            icon.classList.remove("fa-xmark");
            icon.classList.add("fa-bars");

        });

    });


    // Close when clicking outside navbar

    document.addEventListener("click", function (e) {

        if (!navbar.contains(e.target)) {

            navbar.classList.remove("mobile-open");

            const icon = mobileMenuBtn.querySelector("i");

            icon.classList.remove("fa-xmark");
            icon.classList.add("fa-bars");

        }

    });

}