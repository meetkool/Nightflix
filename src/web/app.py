import requests
from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

OMDB_API_KEY = '8cf623f0'

def get_latest_movies():
    response = requests.get('https://api.gdriveplayer.us/v1/movie/newest', params={'limit': 10, 'page': 1, 'order': 'date', 'sort': 'DESC'})
    data = response.json()

    movies = []
    for movie in data:
        title = movie.get('title', '')
        year = movie.get('year', '')
        imdb = movie.get('imdb', '')
        poster = movie.get('poster', '')
        genre = movie.get('genres', '')
        runtime = movie.get('runtimeStr', '')
        director = movie.get('directors', '')
        country = movie.get('countries', '')
        rating = movie.get('imDbRating', '')
        votes = movie.get('imDbVotes', '')

        movies.append({
            'title': title,
            'year': year,
            'imdb': imdb,
            'poster': poster,
            'genre': genre,
            'runtime': runtime,
            'director': director,
            'country': country,
            'rating': rating,
            'votes': votes,
            'sub': '',
            'quality': ''
        })

    return movies


def search_movies(title):
    response = requests.get('http://www.omdbapi.com/', params={'s': title, 'apikey': '8cf623f0'})
    data = response.json()

    movies = []
    if 'Search' in data:
        for result in data['Search']:
            movies.append({
                'title': result['Title'],
                'year': result['Year'],
                'imdb': result['imdbID'],
                'poster': result['Poster'],
                'genre': '',
                'runtime': '',
                'director': '',
                'country': '',
                'rating': '',
                'votes': '',
                'sub': '',
                'quality': ''
            })

    return movies

def get_movie_embed_link(imdb_id):
    embed_link = f'https://vidsrc.me/embed/{imdb_id}/'
    return embed_link

def get_random_movies():
    response = requests.get('https://api.gdriveplayer.us/v1/movie/newest', params={'limit': 10, 'page': 1, 'order': 'date', 'sort': 'DESC'})
    data = response.json()

    movies = []
    random.shuffle(data)
    for movie in data[:6]:
        title = movie.get('title', '')
        year = movie.get('year', '')
        imdb = movie.get('imdb', '')
        poster = movie.get('poster', '')
        genre = movie.get('genres', '')
        runtime = movie.get('runtimeStr', '')
        director = movie.get('directors', '')
        country = movie.get('countries', '')
        rating = movie.get('imDbRating', '')
        votes = movie.get('imDbVotes', '')

        movies.append({
            'title': title,
            'year': year,
            'imdb': imdb,
            'poster': poster,
            'genre': genre,
            'runtime': runtime,
            'director': director,
            'country': country,
            'rating': rating,
            'votes': votes,
            'sub': '',
            'quality': ''
        })

    return movies


@app.route('/', methods=['GET', 'POST'])
def home():
    latest_movies = get_latest_movies()

    if request.method == 'POST':
        title = request.form.get('title')
        return redirect(url_for('search', title=title))

    return render_template('index.html', movies=latest_movies)

@app.route('/search', methods=['GET'])
def search():
    title = request.args.get('title')
    if not title:
        return redirect(url_for('home'))

    movies = search_movies(title)
    return render_template('search.html', movies=movies)

@app.route('/movie/<imdb_id>')
def movie(imdb_id):
    embed_link = get_movie_embed_link(imdb_id)
    related_movies = get_random_movies()
    return render_template('movie.html', embed_link=embed_link, related_movies=related_movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
