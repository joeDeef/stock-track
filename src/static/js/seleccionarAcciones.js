document.addEventListener('DOMContentLoaded', function() {
    const tableRows = document.querySelectorAll('.table-row');

    function actualizarCostoTotal() {
        const cantidad = parseInt(document.getElementById('cantidad').value);
        const precio = parseFloat(document.getElementById('precio_accion').value);
        
        // Tienen valores válidos
        if (!isNaN(cantidad) && !isNaN(precio) && cantidad > 0 && precio > 0) {
            const costoTotal = cantidad * precio;
            document.getElementById('costo_total').value = costoTotal.toFixed(2);
        } else {
            // Si alguno de los campos está vacío o inválido, el costo total se coloca en blanco
            document.getElementById('costo_total').value = '';
        }
    }

    // Cuando seleccionamos una fila de la tabla
    tableRows.forEach(row => {
        row.addEventListener('click', function() {
            tableRows.forEach(row => row.classList.remove('selected'));

            row.classList.add('selected');

            const nombre = row.getAttribute('data-nombre');
            const empresa = row.getAttribute('data-empresa');
            const precio = row.getAttribute('data-precio');

            document.getElementById('nombre').value = nombre;
            document.getElementById('cantidad').value = 1;
            document.getElementById('precio_accion').value = precio;

            actualizarCostoTotal();
        });
    });

    // Escuchamos los cambios en cantidad y precio
    document.getElementById('cantidad').addEventListener('input', actualizarCostoTotal);
    document.getElementById('precio_accion').addEventListener('input', actualizarCostoTotal);

    // Función para obtener el precio de la acción según la fecha seleccionada
    document.getElementById('fecha_compra').addEventListener('change', function() {
        const fechaSeleccionada = this.value;
        const nombreAccion = document.getElementById('nombre').value;

        // Verificar que se haya seleccionado una fecha y que haya un nombre de acción
        if (fechaSeleccionada && nombreAccion) {
            fetch(`/compras/stock_api/obtener_precio_accion_en_fecha?fecha=${fechaSeleccionada}&nombre=${nombreAccion}`)
            .then(response => response.json())
                .then(data => {
                    if (data && data.precio) {
                        // Si obtenemos el precio, lo mostramos en el campo de precio
                        const precio = parseFloat(data.precio);
                        document.getElementById('precio_accion').value = precio.toFixed(2);
                        // Actualizar el costo total
                        actualizarCostoTotal();
                    } else {
                        alert('No se pudo obtener el precio para la fecha seleccionada.');
                    }
                })
                .catch(error => {
                    console.error('Error al obtener el precio:', error);
                    alert('Hubo un error al obtener el precio.');
                });
        }
    });
});
