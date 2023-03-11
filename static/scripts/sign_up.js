const signUpRequirements = document.getElementById('sign-up-requirements');
const password = document.getElementsByClassName('passwordinput form-control')[1];

password.addEventListener('input', () => {
    if (password.value.length > 0 && password.value.length < 8) {
        signUpRequirements.style.color = "black";
    } else {
        signUpRequirements.style.color = "white";
    }
});

document.getElementById('log-in-link').style.display = 'none';

document.getElementById('show-password').addEventListener('click', () => {
    if (password.type === 'password') {
        password.type = 'text';
    } else {
        password.type = 'password';
    }
});