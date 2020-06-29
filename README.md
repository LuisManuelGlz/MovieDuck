# MovieDuck

Este proyecto usa MongoDB como base de datos por lo que es necesario instalar esta base de datos.<br>
[Click para ir al manual de instalación de MongoDB](https://docs.mongodb.com/manual/installation/)

## Instalación
```bash
# Clonamos el repositorio
git clone git@gitlab.com:LuisManuelGlz/movieduck-project.git

# Creamos el entorno virtual
virtualenv -p python3 venv

# Activamos el entorno virtual
source venv/bin/activate

# Instalamos los requerimientos
pip install -r requirements.txt

# Hacemos las migraciones
cd moviesduck_project/
python manage.py migrate

# Corremos el servidor
python manage.py runserver
```
