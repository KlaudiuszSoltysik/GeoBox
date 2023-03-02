var deferredPrompt;
const installBtn = document.getElementById('install-link')

window.addEventListener('beforeinstallprompt', function (event) {
  event.preventDefault();
  deferredPrompt = event;
});

installBtn.addEventListener('click', (e) => {
  deferredPrompt.prompt();
  deferredPrompt.userChoice
    .then((choiceRelult) => {
      if(choiceRelult.outcome==='accepted') {
        installBtn.style.display='none';
      }
      deferredPrompt = null;
    });
});

if (window.matchMedia('(display-mode: standalone)').matches) {  
    installBtn.style.display='none'
}  

const logInForm = document.getElementById('log-in-form');
const logIn = document.getElementById('log-in-link');
const closeLogIn = document.getElementById('close-log-in');

logIn.addEventListener('click', () => {
  logInForm.style.display = "block";
});

closeLogIn.addEventListener('click', () => {
  logInForm.style.display = "none";
});

document.addEventListener('mouseup', (e) => {
  if (!logInForm.contains(e.target)) {
    logInForm.style.display = 'none';
  }
});

document.getElementById('log-in-btn').addEventListener('click', () => {
    logInForm.style.display = 'none';
});