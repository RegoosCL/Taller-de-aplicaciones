function calcularPrecio(dias, precioBase) {
    let precioFinal = precioBase * dias;
    if (dias > 3) {
        precioFinal += (dias - 3) * (precioBase * 0.1);
    }
    return precioFinal.toFixed(0);
}

function actualizarPrecios() {
    const filas = document.querySelectorAll('.fila-bicicleta');
    filas.forEach(fila => {
        const dias = parseInt(fila.querySelector('.dias-arriendo').value) || 0;
        const precioBase = parseFloat(fila.querySelector('.precio-base').textContent);
        const precioFinal = calcularPrecio(dias, precioBase);
        fila.querySelector('.precio-final').textContent = `CLP ${precioFinal}`;
    });
}

function confirmarArriendo(button) {
    const fila = button.closest('.fila-bicicleta');
    const modelo = fila.querySelector('td:nth-child(2)').textContent;
    const dias = fila.querySelector('.dias-arriendo').value;
    const precioBase = fila.querySelector('.precio-base').textContent;
    const precioFinal = fila.querySelector('.precio-final').textContent;
    const nombre = fila.querySelector('.nombre-usuario').value;
    const correo = fila.querySelector('.correo-usuario').value;
    const direccion = fila.querySelector('.direccion-usuario').value;
    const telefono = fila.querySelector('.telefono-usuario').value;

    if (dias <= 0) {
        alert('Por favor, ingrese una cantidad válida de días para el arriendo.');
        return;
    }

    const confirmacion = confirm(`¿Está seguro que desea arrendar la ${modelo} por ${dias} días a un precio de ${precioFinal}?`);
    if (confirmacion) {
        // Enviar datos al servidor
        fetch('/guardar_arriendo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                modelo: modelo,
                precio_base: precioBase,
                dias: dias,
                precio_final: precioFinal,
                nombre: nombre,
                correo: correo,
                direccion: direccion,
                telefono: telefono
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('¡Arriendo confirmado!');
            } else {
                alert('Hubo un error al confirmar el arriendo.');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Hubo un error al confirmar el arriendo.');
        });
    } else {
        alert('El arriendo ha sido cancelado.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.dias-arriendo').forEach(input => {
        input.addEventListener('input', actualizarPrecios);
    });
});

