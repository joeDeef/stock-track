document.addEventListener("DOMContentLoaded", () => {
    const btnComprar = document.getElementById("btn-comprar");
    const cantidad = document.getElementById("cantidad");
    const fechaCompra = document.getElementById("fecha_compra");
    const nombreAccion = document.getElementById("nombre");
    const precioAccion = document.getElementById("precio_accion");
    const totalCompra = document.getElementById("total_compra");

    // Función para actualizar los campos
    const actualizarCampos = () => {
        if (!cantidad.value || !precioAccion.value || !cantidad.checkValidity() || !precioAccion.checkValidity()) {
            return;
        }
        totalCompra.value = "";
    
        const cantidadAcciones = parseInt(cantidad.value, 10);
        const precio = parseFloat(precioAccion.value);
    
        const total = precio * cantidadAcciones;
        totalCompra.value = total.toFixed(3);
    };

    // Detectar cambios
    precioAccion.addEventListener("input", actualizarCampos);
    cantidad.addEventListener("input", actualizarCampos);
});

document.addEventListener("DOMContentLoaded", () => {
    const fechaCompraInput = document.getElementById("fecha_compra");
    
    const today = new Date().toISOString().split("T")[0];
    
    fechaCompraInput.setAttribute("max", today);
});

function confirmarCompra() {
    // Obtenemos los valores del formulario para incluirlos en el mensaje de confirmación
    const nombreAccion = document.getElementById("nombre").value;
    const cantidad = document.getElementById("cantidad").value;
    const fechaCompra = document.getElementById("fecha_compra").value;
    const precioAccion = document.getElementById("precio_accion").value;

    // Verificamos que todos los campos estén llenos
    if (!nombreAccion || !cantidad || !fechaCompra || !precioAccion) {
        alert("Por favor, completa todos los campos antes de realizar un registro.");
        return false;
    }

    // Mensaje de confirmación
    const mensaje = `Estás a punto de registrar ${cantidad} acción(es) de ${nombreAccion} el día ${fechaCompra} con un precio de $${precioAccion}. ¿Deseas continuar?`;

    // Retornamos true si el usuario confirma, false si cancela
    return window.confirm(mensaje);
}