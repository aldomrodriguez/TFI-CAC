const URL = "https://aldomrodriguez.pythonanywhere.com/"


// Capturamos el evento de envío del formulario
document.getElementById('formulario').addEventListener('submit', function (event) {
    event.preventDefault(); // Evitamos que se envie el form 


    var formData = new FormData();
    formData.append('dni', document.getElementById('dni').value);
    formData.append('nombre', document.getElementById('nombre').value);
    formData.append('apellido', document.getElementById('apellido').value);
    formData.append('email', document.getElementById('email').value);
    formData.append('imagen', document.getElementById('imagenUsuario').files[0]);
    
    // Realizamos la solicitud POST al servidor
    fetch(URL + 'usuarios', {
        method: 'POST',
        body: formData // Aquí enviamos formData en lugar de JSON
    })


    //Después de realizar la solicitud POST, se utiliza el método then() para manejar la respuesta del servidor.
    .then(function (response) {
        if (response.ok) { 
            return response.json(); 
        } else {
            // Si hubo un error, lanzar explícitamente una excepción
            // para ser "catcheada" más adelante
            throw new Error('Error al agregar el usuario.');
        }
    })
    
    // Respuesta OK
    .then(function () {
        // En caso de éxito
        alert('Usuario agregado correctamente.');
    })
    .catch(function (error) {
        // En caso de error
        alert('Error al agregar el usuario.');
        console.error('Error:', error);
    })
    .finally(function () {
        // Limpiar el formulario en ambos casos (éxito o error)
        document.getElementById('dni').value = "";
        document.getElementById('nombre').value = "";
        document.getElementById('apellido').value = "";
        document.getElementById('email').value = "";
        document.getElementById('imagenUsuario').value = "";
    });
})
