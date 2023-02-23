let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        deferredPrompt = e;
    });

const installApp = document.getElementById('install-button');

installApp.addEventListener('click', async () => {
    if (deferredPrompt !== null) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') {
            deferredPrompt = null;
        }
    }
});

const logInForm = document.getElementById('log-in-form');
const logIn = document.getElementById('log-in-button');
const closeLogIn = document.getElementById('close-log-in');

logIn.addEventListener('click',  () => {
    logInForm.style.display = "block";
});

closeLogIn.addEventListener('click',  () => {
    logInForm.style.display = "none";
});

document.addEventListener('mouseup', function(e) {
    if (!logInForm.contains(e.target)) {
     logInForm.style.display = 'none';
    }
});
