import json
from pathlib import Path

from flask import Flask, jsonify

# Creación de la aplicación Flask
app = Flask(__name__)
MOVIES_FILE = Path(__file__).resolve().parent / 'data' / 'datos_movies.json'

# Definición de la ruta (/movies) con un método GET
@app.route('/movies', methods=['GET'])
def obtener_movies():
    with MOVIES_FILE.open(encoding='utf-8') as movies_file:
        movies = json.load(movies_file)
    return jsonify(movies)


if __name__ == '__main__':
    app.run(debug=True, port=5000)