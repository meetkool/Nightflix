import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
            'genre': movie['genre'],
            'runtime': movie['runtime'],
            'director': movie['director'],
            'country': movie['country'],
            'rating': movie['rating'],
            'votes': movie['votes'],
            'sub': movie['sub'],
            'quality': movie['quality']
        })

    return movies

def search_movies(title):
    response = requests.get(f'https://imdb-api.com/en/API/SearchTitle/k_c7k913z5/{title}')
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
    embed_link = f'https://vidsrc.me/embed/{imdb_id}/'
    return embed_link

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
    return render_template('movie.html', embed_link=embed_link)

if __name__ == '__main__':
    app.run(debug=True)
