import json
from collections import Counter, defaultdict
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st


DATA_FILE = Path(__file__).resolve().parent / 'data' / 'datos_movies.json'


@st.cache_data
def load_movies(file_modified_at):
    with DATA_FILE.open(encoding='utf-8') as movies_file:
        return json.load(movies_file)


st.set_page_config(page_title='Dashboard de películas', layout='wide')
st.title('Análisis de películas')

try:
    movies = load_movies(DATA_FILE.stat().st_mtime_ns)
except (OSError, json.JSONDecodeError) as error:
    st.error(f'No se pudieron cargar los datos de películas: {error}')
    st.stop()

if not movies:
    st.info('No hay películas registradas para mostrar.')
    st.stop()

annual_revenue = defaultdict(list)
for movie in movies:
    year = movie.get('release_year')
    if year is None:
        continue
    if year not in annual_revenue:
        annual_revenue[year] = []
    revenue = movie.get('box_office_usa_usd')
    if revenue is not None:
        annual_revenue[year].append(revenue)

years = sorted(annual_revenue)
minimums = [min(annual_revenue[year]) if annual_revenue[year] else None for year in years]
maximums = [max(annual_revenue[year]) if annual_revenue[year] else None for year in years]

st.subheader('Evolución de taquilla por año de estreno')
if any(value is not None for value in maximums):
    revenue_figure = go.Figure()
    revenue_figure.add_trace(go.Scatter(
        x=years,
        y=maximums,
        mode='lines+markers',
        name='Máximo',
        line={'color': '#2457C5'},
        hovertemplate='Año %{x}<br>Máximo: $%{y:,.0f}<extra></extra>',
    ))
    revenue_figure.add_trace(go.Scatter(
        x=years,
        y=minimums,
        mode='lines',
        name='Mínimo',
        line={'color': '#2457C5', 'width': 0},
        fill='tonexty',
        fillcolor='rgba(36, 87, 197, 0.20)',
        connectgaps=False,
        hovertemplate='Año %{x}<br>Mínimo: $%{y:,.0f}<extra></extra>',
    ))
    revenue_figure.update_layout(
        xaxis_title='Año de estreno',
        yaxis_title='Taquilla registrada (USD)',
        yaxis_tickprefix='$',
        yaxis_tickformat=',.0f',
        hovermode='x unified',
        legend_title_text='Rango anual',
    )
    st.plotly_chart(revenue_figure, width='stretch')
    st.caption(
        'La banda representa el mínimo y el máximo de taquilla por año. '
        'Los registros sin importe no se incluyen en el cálculo.'
    )
else:
    st.info('No hay importes de taquilla registrados para mostrar.')

st.subheader('Películas registradas por género')
genre_counts = Counter(
    movie.get('genre') or 'Sin género'
    for movie in movies
)
genre_figure = go.Figure(data=[go.Pie(
    labels=list(genre_counts),
    values=list(genre_counts.values()),
    hole=0.35,
    textinfo='label+value+percent',
)])
genre_figure.update_layout(showlegend=True)
st.plotly_chart(genre_figure, width='stretch')

durations = [
    movie['duration_minutes']
    for movie in movies
    if isinstance(movie.get('duration_minutes'), (int, float))
]

st.subheader('Distribución de la duración de las películas')
if durations:
    duration_figure = go.Figure(data=[go.Histogram(
        x=durations,
        nbinsx=8,
        marker_color='#D1495B',
        hovertemplate='Duración: %{x} min<br>Películas: %{y}<extra></extra>',
    )])
    duration_figure.update_layout(
        xaxis_title='Duración (minutos)',
        yaxis_title='Número de películas',
        bargap=0.08,
    )
    st.plotly_chart(duration_figure, width='stretch')
else:
    st.info('No hay duraciones registradas para mostrar.')