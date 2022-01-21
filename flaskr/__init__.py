import os

from flask import Flask


def create_app(test_config=None):
    # Crear y configurar la aplicacion
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        )

    if test_config is None:
        # Cargar el archivo cofig, solo si exite, cuando no se ralicen pruebas
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Cargar el archivo config si se pasa como argumento
        app.config.from_mapping(test_config)

    # Asegurarse de que exite el directorio instancia
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # pagina simple que dice Hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

