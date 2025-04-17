# Movie Recommendation System

A web-based movie recommendation system that suggests movies based on user input. The system uses content-based filtering to find similar movies based on various features like cast, crew, keywords, and genres.

## Features

- Search movies by title or keywords
- Get movie recommendations based on content similarity
- View movie details including:
  - Title and year
  - Rating
  - Overview
  - Genres
  - Poster image
- Simple and intuitive user interface
- Real-time search results
- Popular and recent movie listings
- Genre-based filtering

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Required Packages

- Flask
- pandas
- scikit-learn
- numpy
- ast

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Movie-Recommender-System.git
cd Movie-Recommender-System
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install flask pandas scikit-learn numpy
```

4. Download the dataset:
   - Download the TMDB 5000 Movies dataset from [Kaggle](https://www.kaggle.com/tmdb/tmdb-movie-metadata)
   - Place the following files in the project directory:
     - `tmdb_5000_movies.csv`
     - `tmdb_5000_credits.csv`

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## How to Use

1. Enter a movie title or keyword in the search box
2. Click the search button or press Enter
3. View the list of recommended movies
4. Each recommendation shows:
   - Movie title
   - Ranking
   - Year
   - Rating
   - Overview
   - Genres
   - Poster image

## Project Structure

```
Movie-Recommender-System/
├── app.py                 # Main application file
├── templates/
│   └── index.html         # Frontend template
├── tmdb_5000_movies.csv   # Movie dataset
└── tmdb_5000_credits.csv  # Credits dataset
```

## How It Works

1. The system loads and processes movie data from the TMDB dataset
2. It creates a content-based similarity matrix using:
   - Movie cast (top 3 actors)
   - Director
   - Keywords
   - Genres
3. When a user searches for a movie:
   - First tries to find exact matches in movie titles
   - If no exact matches, uses content similarity to find recommendations
4. Returns a list of recommended movies based on the search

## API Endpoints

- `/` - Home page
- `/recommend` - Get movie recommendations (POST)
- `/movie/<title>` - Get movie details (GET)
- `/popular` - Get popular movies (GET)
- `/recent` - Get recent movies (GET)
- `/genre/<genre>` - Get movies by genre (GET)
- `/autocomplete` - Get search suggestions (GET)

## Troubleshooting

If you encounter any issues:

1. Make sure all required packages are installed
2. Verify that the dataset files are in the correct location
3. Check if the Flask server is running
4. Ensure you have an active internet connection for loading movie posters

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- TMDB for providing the movie dataset
- Flask for the web framework
- scikit-learn for the machine learning algorithms
- Bootstrap for the UI components
- Font Awesome for the icons
