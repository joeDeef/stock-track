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

    tableRows.forEach(row => {
        // Agregamos un evento de clic a cada fila
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

    document.getElementById('cantidad').addEventListener('input', actualizarCostoTotal);
    document.getElementById('precio_accion').addEventListener('input', actualizarCostoTotal);
});
