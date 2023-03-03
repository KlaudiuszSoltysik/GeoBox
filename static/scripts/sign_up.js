const signUpRequirements = document.getElementById('sign-up-requirements');
const password = document.getElementById('password-input');

password.addEventListener('input', () => {
  if(password.value.length > 0 && password.value.length < 8) {
    signUpRequirements.style.color = "black";
  } else {
    signUpRequirements.style.color = "white";
  }
})

document.getElementById('log-in-btn').style.display = 'none';

document.getElementById('show-password').addEventListener('click', () => {
  var password = document.getElementById('password-input');
  if (password.type === 'password') {
    password.type = 'text';
  } else {
    password.type = 'password';
  }
});