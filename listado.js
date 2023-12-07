const URL = "https://aldomrodriguez.pythonanywhere.com/"


// Realizamos la solicitud GET al servidor para obtener todos los productos
fetch(URL + 'usuarios')
    .then(function (response) {
        if (response.ok) {
            return response.json(); 
    } else {
            // Si hubo un error, lanzar explícitamente una excepción
            // para ser "catcheada" más adelante
            throw new Error('Error al obtener los usuarios.');
        }
    })
    .then(function (data) {
        let tablaUsuarios = document.getElementById('tablaUsuarios');


        // Iteramos sobre los productos y agregamos filas a la tabla
        for (let usuario of data) {
            let fila = document.createElement('tr');
            fila.innerHTML = '<td>' + usuario.dni + '</td>' +
                '<td>' + usuario.nombre + '</td>' +
                '<td>' + usuario.apellido + '</td>' +
                '<td>' + usuario.email + '</td>' +
                // Mostrar miniatura de la imagen
                '<td><img src=https://www.pythonanywhere.com/user/aldomrodriguez/files/home/aldomrodriguez/static/img/' + usuario.imagen_url +' alt="Imagen del usuario" style="width: 100px;"></td>';
            
            //Una vez que se crea la fila con el contenido del producto, se agrega a la tabla utilizando el método appendChild del elemento tablaProductos.
            tablaUsuarios.appendChild(fila);
        }
    })
    .catch(function (error) {
        // En caso de error
        alert('Error al agregar el usuario.');
        console.error('Error:', error);
    })
