<div align="center">

  <img src="https://user-images.githubusercontent.com/37312790/114077634-def5dc80-985c-11eb-8071-c51be53f1c5f.png" alt="MovieDuck logo" width=200 />

  # MovieDuck

</div>

## Instalación
```bash
# Clonamos el repositorio
git clone https://github.com/LuisManuelGlz/MovieDuck.git

# Entramos al proyecto
cd MovieDuck

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
