from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Load data
movies_df = pd.read_csv("tmdb_5000_movies.csv")
credits_df = pd.read_csv("tmdb_5000_credits.csv")

# Merge data
credits_df.columns = ['id','tittle','cast','crew']
movies_df = movies_df.merge(credits_df, on="id")

# Process data
features = ["cast", "crew", "keywords", "genres"]
for feature in features:
    movies_df[feature] = movies_df[feature].apply(literal_eval)

# Get director
movies_df["director"] = movies_df["crew"].apply(lambda x: next((i["name"] for i in x if i["job"] == "Director"), np.nan))

# Get top 3 cast and keywords
for feature in ["cast", "keywords", "genres"]:
    movies_df[feature] = movies_df[feature].apply(lambda x: [i["name"] for i in x][:3] if isinstance(x, list) else [])

# Clean data
for feature in ['cast', 'keywords', 'director', 'genres']:
    movies_df[feature] = movies_df[feature].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x] if isinstance(x, list) else str.lower(x.replace(" ", "")) if isinstance(x, str) else "")

# Create soup for similarity
movies_df["soup"] = movies_df.apply(lambda x: ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres']), axis=1)

# Create similarity matrix
count_vectorizer = CountVectorizer(stop_words="english")
count_matrix = count_vectorizer.fit_transform(movies_df["soup"])
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Create indices
movies_df = movies_df.reset_index()
indices = pd.Series(movies_df.index, index=movies_df['title'])

def get_recommendations(title):
    try:
        # Convert to lowercase
        title = title.lower()
        
        # Find matching movies
        matching_movies = movies_df[movies_df['title'].str.lower().str.contains(title)]
        
        if len(matching_movies) > 0:
            return matching_movies['title'].tolist()
        
        # If no matches, try content similarity
        idx = indices.get(title, None)
        if idx is not None:
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:11]
            movies_indices = [ind[0] for ind in sim_scores]
            return movies_df["title"].iloc[movies_indices].tolist()
        
        return []
    except:
        return []

def get_movie_details(title):
    try:
        movie = movies_df[movies_df['title'] == title].iloc[0]
        return {
            'title': movie['title'],
            'year': int(movie['year']) if pd.notna(movie['year']) else None,
            'rating': round(movie['vote_average'], 1) if pd.notna(movie['vote_average']) else None,
            'overview': movie['overview'],
            'genres': [g['name'] for g in literal_eval(movie['genres'])] if isinstance(movie['genres'], str) else [],
            'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if pd.notna(movie['poster_path']) else None
        }
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie_title']
    recommendations = get_recommendations(movie_title)
    return jsonify(recommendations)

@app.route('/movie/<title>', methods=['GET'])
def movie_details(title):
    details = get_movie_details(title)
    return jsonify(details) if details else jsonify({'error': 'Movie not found'}), 404

@app.route('/popular', methods=['GET'])
def popular():
    popular = movies_df.sort_values('popularity', ascending=False).head(10)
    return jsonify(popular['title'].tolist())

@app.route('/recent', methods=['GET'])
def recent():
    recent = movies_df.sort_values('release_date', ascending=False).head(10)
    return jsonify(recent['title'].tolist())

@app.route('/genre/<genre>', methods=['GET'])
def genre(genre):
    genre_movies = movies_df[movies_df['genres'].apply(lambda x: genre.lower() in str(x).lower())]
    return jsonify(genre_movies['title'].tolist())

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])
    
    matches = movies_df[movies_df['title'].str.lower().str.contains(query)]
    suggestions = matches['title'].tolist()[:10]
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True) 