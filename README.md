# Gestor de usuarios

Trabajo final integrador del curso de Desarrollo Full Stack Python de Codo a Codo: un CRUD de usuarios.

- **Backend:** API en Flask (`Programa.py`) con MySQL.
- **Frontend:** páginas en HTML y JavaScript para dar de alta, listar, modificar y eliminar.

## Cómo correrlo

La conexión a MySQL se toma de variables de entorno:

```bash
export MYSQL_HOST=... MYSQL_USER=... MYSQL_PASSWORD=... MYSQL_DATABASE=...
pip install flask flask-cors mysql-connector-python
python Programa.py
```
