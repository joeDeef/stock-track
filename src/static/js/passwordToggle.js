document.addEventListener("DOMContentLoaded", function () {
    const toggleButtons = document.querySelectorAll(".toggle-password");

    toggleButtons.forEach(button => {
        button.addEventListener("click", function () {
            const inputId = this.getAttribute("data-input");
            const passwordInput = document.getElementById(inputId);

            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                this.textContent = "Ocultar";
            } else {
                passwordInput.type = "password";
                this.textContent = "Mostrar";
            }
        });
    });
});
