const URL = "http://127.0.0.1:5000/"


const app = Vue.createApp({ 
    data() {
        return {
            dni: '',
            nombre: '',
            apellido: '',
            email: '',
            imagen_url: '',
            imagenUrlTemp: null,
            mostrarDatosUsuario: false,
        };
    },


    methods: {
        obtenerUsuario() {
            fetch(URL + 'usuarios/' + this.dni)
                .then(response =>  {
                    if (response.ok) {
                        return response.json()
                    } else {
                        //Si la respuesta es un error, lanzamos una excepción para ser "catcheada" más adelante en el catch.
                        throw new Error('Error al obtener los datos del usuario.')
                    }
                })


                .then(data => {
                    this.nombre = data.nombre;
                    this.apellido = data.apellido;
                    this.email = data.email;
                    this.imagen_url =  data.imagen_url;
                    this.mostrarDatosUsuario = true;
                })
                .catch(error => {
                    console.log(error);
                    alert('DNI no encontrado.');
                })
        },
        seleccionarImagen(event) {
            const file = event.target.files[0];
            this.imagenSeleccionada = file;
            this.imagenUrlTemp = URL.createObjectURL(file); // Crea una URL temporal para la vista previa
        },
        guardarCambios() {
            const formData = new FormData();
            formData.append('dni', this.dni);
            formData.append('nombre', this.nombre);
            formData.append('apellido', this.apellido);
            formData.append('email', this.email);


            if (this.imagenSeleccionada) {
                formData.append('imagen', this.imagenSeleccionada, this.imagenSeleccionada.name);
            }


            //Utilizamos fetch para realizar una solicitud PUT a la API y guardar los cambios.
            fetch(URL + 'usuarios/' + this.dni, {
                method: 'PUT',
                body: formData,
            })
            .then(response => {
                //Si la respuesta es exitosa, utilizamos response.json() para parsear la respuesta en formato JSON.
                if (response.ok) {
                    return response.json()
                } else {
                    //Si la respuesta es un error, lanzamos una excepción.
                    throw new Error('Error al guardar los cambios del usuario.')
                }
            })
            .then(data => {
                alert('Usuario actualizado correctamente.');
                this.limpiarFormulario();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al actualizar el usuario.');
            });
        },
        limpiarFormulario() {
            this.dni = '';
            this.nombre = '';
            this.apellido = '';
            this.email = '';
            this.imagen_url = '';
            this.imagenSeleccionada = null;
            this.imagenUrlTemp = null;
            this.mostrarDatosUsuario = false;
        }
    }
});


app.mount('#app');
