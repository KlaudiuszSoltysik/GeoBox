var deferredPrompt;
const installBtn = document.getElementById("install-link")

window.addEventListener("beforeinstallprompt", function(event) {
    event.preventDefault();
    deferredPrompt = event;
});

installBtn.addEventListener("click", (e) => {
    deferredPrompt.prompt();
    deferredPrompt.userChoice
        .then((choiceRelult) => {
            if (choiceRelult.outcome === "accepted") {
                installBtn.style.display = "none";
            }
            deferredPrompt = null;
        });
});

if (window.matchMedia("(display-mode: standalone)").matches) {
    document.getElementById("install-link").remove()
}

const logInForm = document.getElementById("log-in-form");
var logIn = document.getElementsByClassName("log-in-link");
const closeLogIn = document.getElementById("close-log-in");


for (const element of logIn) {
    element.addEventListener("click", () => {
        logInForm.style.display = "block";
    })
}

closeLogIn.addEventListener("click", () => {
    logInForm.style.display = "none";
});

document.addEventListener("mouseup", (e) => {
    if (!logInForm.contains(e.target)) {
        logInForm.style.display = "none";
    }
});

document.getElementById("log-in-btn").addEventListener("click", () => {
    logInForm.style.display = "none";
});