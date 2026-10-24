import json
import re
from pathlib import Path

from flask import Flask, jsonify, request

# Creación de la aplicación Flask
app = Flask(__name__)
MOVIES_FILE = Path(__file__).resolve().parent / 'data' / 'datos_movies.json'
FILTER_PATTERN = re.compile(r'(?<!\S)([A-Za-z_]\w*):')


def _parse_filters(query):
    matches = list(FILTER_PATTERN.finditer(query))
    filters = []
    for index, match in enumerate(matches):
        value_start = match.end()
        value_end = matches[index + 1].start() if index + 1 < len(matches) else len(query)
        value = query[value_start:value_end].strip()
        if value:
            filters.append((match.group(1), value))
    return filters


def _iter_movie_fields(value):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            yield key, nested_value
            yield from _iter_movie_fields(nested_value)
    elif isinstance(value, list):
        for nested_value in value:
            yield from _iter_movie_fields(nested_value)


def _matches_filter(movie, key, expected_value):
    expected_value = expected_value.casefold()
    for movie_key, value in _iter_movie_fields(movie):
        if str(movie_key).casefold() != key.casefold():
            continue
        if value is None:
            value_text = 'null'
        elif isinstance(value, bool):
            value_text = str(value).lower()
        elif isinstance(value, (dict, list)):
            value_text = json.dumps(value, ensure_ascii=False)
        else:
            value_text = str(value)
        if expected_value in value_text.casefold():
            return True
    return False

# Definición de la ruta (/movies) con un método GET
@app.route('/movies', methods=['GET'])
def obtener_movie_id():
    with MOVIES_FILE.open(encoding='utf-8') as movies_file:
        movies = json.load(movies_file)
    query = request.args.get('q')
    if query:
        filters = _parse_filters(query)
        movies = [
            movie for movie in movies
            if all(_matches_filter(movie, key, value) for key, value in filters)
        ]
    return jsonify(movies)


if __name__ == '__main__':
    app.run(debug=True, port=5000)