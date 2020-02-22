## Antes de empezar

Para utilizar este proyecto es necesario ejecutar los siguientes comandos.

```bash
# Creamos el entorno virtual
virtualenv -p python3 venv

# Activamos el entorno virtual
source venv/bin/activate

# Instalamos los requerimientos
pip install -r requirements.txt

# Hacemos las migraciones
python manage.py migrate

# Corremos el servidor
python manage.py runserver
```
