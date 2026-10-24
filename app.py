from flask import Flask, jsonify

# Creación de la aplicación Flask
app = Flask(__name__)

# Definición de la ruta (/movies) con un método GET
@app.route('/movies', methods=['GET'])
def obtener_movies():
    # Creamos una lista con los datos de varias películas
    movies = [
        {
            "id_movie": "MOV-2026-894021",
            "title": "The Matrix",
            "director": "Lana Wachowski, Lilly Wachowski", 
            "release_year": 1999,
            "genre": "Science Fiction"  
        }
    ]

    # Devolvemos la lista de películas y omitimos el código de estado (200 por defecto)
    return jsonify(movies)


if __name__ == '__main__':
    app.run(debug=True, port=5000)