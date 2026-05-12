const API_KEY = '495352769dbc05d7c88f80f7499e823e';
const BASE_URL = 'https://api.themoviedb.org/3';
const IMG_PATH = 'https://image.tmdb.org/t/p/w500';

const PREFERRED = {
    //  Walter Mitty | Superman 2025 | Spider-Man NWH | Bruce Almighty | Back to the Future | The Greatest Showman
    hollywood: [116745, 1061474, 634649, 310, 105, 316029],

    //  Demon Slayer Infinity Castle | Kung Fu Panda | LEGO Batman | Tangled | Fantastic Mr. Fox | Mahavatar Narsimha
    animated: [1311031, 9502, 324849, 38757, 10315, 1383072],

    //  RRR | Jai Bhim | Thozha/Oopiri | Kalki 2898 AD | Sitaare Zameen Par | Nanban
    indian: [579974, 855400, 369925, 801688, 1190511, 69537]
};

async function fetchMovies(endpoint) {
    try {
        const res = await fetch(`${BASE_URL}${endpoint}${endpoint.includes('?') ? '&' : '?'}api_key=${API_KEY}`);
        return await res.json();
    } catch (e) {
        console.error("API Error:", e);
        return null;
    }
}

async function fetchMovieById(id) {
    return await fetchMovies(`/movie/${id}`);
}

function renderMovieCard(movie, container, basePath = '') {
    const year = movie.release_date ? movie.release_date.split('-')[0] : 'N/A';
    const poster = movie.poster_path ? IMG_PATH + movie.poster_path : `${basePath}movies/photos/logo.png`;

    const card = `
        <div class="MainMvContainer">
            <div class="MovieContainer">
                <img class="movieImg" src="${poster}" alt="${movie.title}">
                <div class="movieDetails">
                    <a href="${basePath}movies/movie-details.html?tmdbId=${movie.id}" class="movieName">${movie.title}</a>
                    <p class="movieGenre">${year}</p>
                    <p class="movieRating">⭐ ${movie.vote_average ? movie.vote_average.toFixed(1) : 'N/A'}</p>
                </div>
            </div>
            <p class="movieDesc">${movie.overview ? movie.overview.substring(0, 110) + '...' : 'No description available.'}</p>
        </div>
    `;
    container.innerHTML += card;
}
