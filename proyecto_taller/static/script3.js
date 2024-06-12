const $btnSignUp= document.querySelector('.sign-up-btn'),
      $btnSignIn = document.querySelector('.sign-in-btn'),  
      $signIn = document.querySelector('.sign-in'),
      $signUp  = document.querySelector('.sign-up');

document.addEventListener('click', e => {
    if (e.target === $btnSignUp || e.target === $btnSignIn) {
        $signUp.classList.toggle('active');
        $signIn.classList.toggle('active')
    }
});

// Selección de elementos
const modalButton = document.getElementById('modalBtn');
const closeButton = document.querySelector('.closeIcon');
const tryAgainButton = document.getElementById('okBtn');
const modal = document.querySelector('.modal');

// Función para mostrar el modal
function showModal() {
  modal.classList.add('active');
}

// Función para ocultar el modal
function hideModal() {
  modal.classList.remove('active');
}

// Eventos de clic
modalButton.addEventListener('click', showModal);
closeButton.addEventListener('click', hideModal);
tryAgainButton.addEventListener('click', hideModal);

// Evento de clic en la ventana para ocultar el modal
window.addEventListener('click', event => {
  if (event.target === modal) {
    hideModal();
  }
});