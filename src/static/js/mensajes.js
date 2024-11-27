document.addEventListener('DOMContentLoaded', function() {
    var mensajes = document.querySelectorAll('.mensaje');
    mensajes.forEach(function(mensaje) {
        mensaje.style.display = 'block';
        setTimeout(function() {
            mensaje.style.display = 'none';
        }, 3000); // Ocultar después de 3 segundos
    });
});
