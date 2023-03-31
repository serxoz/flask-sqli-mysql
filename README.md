# Ejemplo de aplicación flask vulnerable a sqli con mariadb

Esta aplicación nos sirve para jugar con las inyecciones SQL. Tiene una
ruta que simula un login.

## Instalación
- Configuración: modifique la variable *db_cred* en app.py con los valores
de conexión al mariadb y cree la base de datos con el mismo nombre que db_cred["name"].

- Entorno virtual:
```bash
python -m venv venv
source venv/bin/activate
```

- Instalación de dependencias:
```bash
pip install -r requirements.txt
```

- Ejecución de la aplicación:
```bash
python app.py
```

## Pruebas

Utilizando cURL puede probar a *hacer login*:
```bash
curl -d "email=john.doe@zmail.com&password=john@123" http://127.0.0.1:5000/sqli/login
```

Inyección SQL:
```bash
curl -d "email=john.doe@zmail.com';-- &password=fakepasswd" http://127.0.0.1:5000/sqli/login
```
