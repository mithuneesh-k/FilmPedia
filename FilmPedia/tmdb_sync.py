import urllib.request
import urllib.parse
import json
import os
import time

API_KEY = "495352769dbc05d7c88f80f7499e823e"
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE_URL = "https://image.tmdb.org/t/p/w500"

def get_json(url):
    retries = 3
    for i in range(retries):
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            if i == retries - 1:
                raise e
            time.sleep(2)

# List of movies to fetch
movies_to_sync = [
    {"id": "brucealmighty", "query": "Bruce Almighty"},
    {"id": "demonslayer", "query": "Demon Slayer: Kimetsu no Yaiba - The Movie: Mugen Train"}, # Using a known movie since Infinity Castle is upcoming
    {"id": "jaibhim", "query": "Jai Bhim"},
    {"id": "kalki", "query": "Kalki 2898 AD"},
    {"id": "kungfupanda", "query": "Kung Fu Panda"},
    {"id": "legobatman", "query": "The Lego Batman Movie"},
    {"id": "maaveeran", "query": "Maaveeran"},
    {"id": "minecraft", "query": "A Minecraft Movie"},
    {"id": "nanban", "query": "Nanban"},
    {"id": "narshima", "query": "Narasimha"}, 
    {"id": "rrr", "query": "RRR"},
    {"id": "serendipity", "query": "Serendipity"},
    {"id": "spiderman", "query": "Spider-Man: No Way Home"},
    {"id": "spiderverse", "query": "Spider-Man: Across the Spider-Verse"},
    {"id": "superman", "query": "Superman"},
    {"id": "tangled", "query": "Tangled"},
    {"id": "thozha", "query": "Thozha"},
    {"id": "waltermitty", "query": "The Secret Life of Walter Mitty"}
]

new_movies_data = []

for m in movies_to_sync:
    print(f"Fetching data for: {m['query']}...")
    
    try:
        # 1. Search
        query_encoded = urllib.parse.quote(m['query'])
        search_url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query_encoded}"
        search_res = get_json(search_url)
        
        if not search_res.get('results'):
            print(f"No results found for {m['query']}")
            continue
            
        # Try to find the best match (closest title or most popular)
        tmdb_movie = search_res['results'][0]
        movie_id = tmdb_movie['id']
        
        # 2. Get Details (Credits + Videos)
        detail_url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits,videos"
        movie_details = get_json(detail_url)
        
        # 3. Extract Data
        genres = " • ".join([g['name'] for g in movie_details.get('genres', [])])
        
        cast = []
        for member in movie_details.get('credits', {}).get('cast', [])[:10]:
            cast.append(f"{member['name']} as {member['character']}")
            
        crew = []
        for member in movie_details.get('credits', {}).get('crew', []):
            if member['job'] == 'Director':
                crew.append(f"Directed by {member['name']}")
            elif member['job'] == 'Producer':
                 crew.append(f"Produced by {member['name']}")
                 
        # Get Trailer
        trailer_url = ""
        for video in movie_details.get('videos', {}).get('results', []):
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
                break

        new_movies_data.append({
            "id": m['id'],
            "title": movie_details.get('title'),
            "image": f"{IMG_BASE_URL}{movie_details.get('poster_path')}" if movie_details.get('poster_path') else "photos/logo.png",
            "genre": genres,
            "rating": f"TMDb: {movie_details.get('vote_average')}",
            "description": movie_details.get('overview'),
            "trailerUrl": trailer_url,
            "cast": cast,
            "crew": list(set(crew[:3])),
            "story": movie_details.get('overview'),
            "reviews": [], 
            "watchersGuide": [
                f"Runtime: {movie_details.get('runtime')} minutes",
                f"Release Date: {movie_details.get('release_date')}"
            ],
            "funFacts": []
        })
        time.sleep(1) # Small delay to be nice to the API
    except Exception as e:
        print(f"Error processing {m['query']}: {e}")

# Ensure directory exists
os.makedirs('movies', exist_ok=True)

with open('movies/movies.json', 'w', encoding='utf-8') as f:
    json.dump(new_movies_data, f, indent=2)

print(f"\nSuccessfully synced {len(new_movies_data)} movies to movies/movies.json!")
