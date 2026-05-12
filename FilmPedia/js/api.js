const API_KEY = '495352769dbc05d7c88f80f7499e823e';
const BASE_URL = 'https://api.themoviedb.org/3';
const IMG_PATH = 'https://image.tmdb.org/t/p/w500';

const PREFERRED = {
    hollywood: [116745, 1084736, 634649, 315, 11354, 335977],
    animated: [508439, 9502, 1374523, 569094, 324849, 38757],
    indian: [579047, 81839, 870357, 801688, 379291, 1040523]
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
