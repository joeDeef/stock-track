document.addEventListener("DOMContentLoaded", () => {
    const btnComprar = document.getElementById("btn-comprar");
    const cantidad = document.getElementById("cantidad");
    const fechaCompra = document.getElementById("fecha_compra");
    const nombreAccion = document.getElementById("nombre");
    const precioAccion = document.getElementById("precio_accion");
    const totalCompra = document.getElementById("total_compra");

    // Función para obtener el precio de la acción en una fecha
    const obtenerPrecioAccion = async (fecha, nombreAccion) => {
        try {
            const response = await fetch(`/compras/api/precio_accion?fecha=${fecha}&nombre_accion=${nombreAccion}`);
            if (!response.ok) {
                throw new Error("Error al obtener el precio de la acción");
            }
            const data = await response.json();
            return data.precio;  // Suponiendo que el JSON contiene un campo "precio"
        } catch (error) {
            console.error(error);
        }
    };

    // Función para actualizar los campos
    const actualizarCampos = async () => {
        // Borrar los valores de los campos no editables cuando uno de los campos editables cambie
        precioAccion.value = "";
        totalCompra.value = "";

        const fecha = fechaCompra.value;
        const cantidadAcciones = parseInt(cantidad.value, 10);
        const nombre = nombreAccion.value.trim();

        if (fecha && cantidadAcciones > 0 && nombre) {
            const precio = await obtenerPrecioAccion(fecha, nombre);
            
            if (precio) {
                // Actualizar el primer campo no editable con el precio
                precioAccion.value = `$${precio.toFixed(2)}`;
                
                // Calcular el total
                const total = precio * cantidadAcciones;
                totalCompra.value = `$${total.toFixed(2)}`;
            }
        }
    };

    // Detectar cambios en los campos de cantidad, nombre o fecha
    cantidad.addEventListener("input", actualizarCampos);
    fechaCompra.addEventListener("input", actualizarCampos);
    nombreAccion.addEventListener("input", actualizarCampos);
});

function confirmarCompra() {
    // Obtenemos los valores del formulario para incluirlos en el mensaje de confirmación
    const nombreAccion = document.getElementById("nombre").value;
    const cantidad = document.getElementById("cantidad").value;
    const fechaCompra = document.getElementById("fecha_compra").value;

    // Verificamos que todos los campos estén llenos
    if (!nombreAccion || !cantidad || !fechaCompra) {
        alert("Por favor, completa todos los campos antes de comprar.");
        return false;
    }

    // Mensaje de confirmación
    const mensaje = `Estás a punto de comprar ${cantidad} acciones de ${nombreAccion} el día ${fechaCompra}. ¿Deseas continuar?`;

    // Retornamos true si el usuario confirma, false si cancela
    return window.confirm(mensaje);
}