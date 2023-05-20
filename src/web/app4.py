import requests
from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

IMDB_API_KEY = 'k_5pjllrms'

def get_latest_movies():
    response = requests.get('https://api.gdriveplayer.us/v1/movie/newest', params={'limit': 10, 'page': 1, 'order': 'date', 'sort': 'DESC'})
    data = response.json()

    movies = []
    for movie in data:
        movies.append({
            'title': movie['title'],
            'year': movie['year'],
            'imdb': movie['imdb'],
            'poster': movie['poster'],
            'genre': movie.get('genres', ''),
            'runtime': movie.get('runtimeStr', ''),
            'director': movie.get('directors', ''),
            'country': movie.get('countries', ''),
            'rating': movie.get('imDbRating', ''),
            'votes': movie.get('imDbVotes', ''),
            'sub': '',
            'quality': ''
        })

    return movies

def search_movies(title):
    response = requests.get(f'https://imdb-api.com/en/API/SearchTitle/{IMDB_API_KEY}/{title}')
    data = response.json()

    movies = []
    if 'results' in data:
        for result in data['results']:
            if result['resultType'] == 'Title':
                movies.append({
                    'title': result['title'],
                    'year': result['description'],
                    'imdb': result['id'],
                    'poster': result['image'],
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
    embed_link = f'http://database.gdriveplayer.us/player.php?imdb={imdb_id}'
    return embed_link

def get_random_movies():
    response = requests.get(f'https://imdb-api.com/en/API/MostPopularMovies/{IMDB_API_KEY}')
    data = response.json()

    movies = []
    if 'items' in data:
        random.shuffle(data['items'])
        for item in data['items'][:6]:
            movies.append({
                'title': item['title'],
                'year': item['year'],
                'imdb': item['id'],
                'poster': item['image'],
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
    app.run(host='0.0.0.0', port=5001, debug=True)
