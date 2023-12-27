#  Copyright (c) 2023 Edgeburn Media. All rights reserved.
import os
from typing import List

import tmdbsimple as tmdb
from loguru import logger
from plexapi.library import LibrarySection, Guid
from plexapi.server import PlexServer
from plexapi.video import Movie

# TMDB
tmdb.API_KEY = os.environ.get("TMDB_API_KEY")

# Plex
PLEX_BASE_URL = os.environ.get("PLEX_BASE_URL")
PLEX_AUTH_TOKEN = os.environ.get("PLEX_AUTH_TOKEN")
plex = PlexServer(PLEX_BASE_URL, PLEX_AUTH_TOKEN)


def _sample_debug():
    movie = tmdb.Movies(695721)
    response = movie.info()
    print(movie.title)


def get_tmdb_id(movie) -> str:
    """
    Get TMDB id for a given movie. If multiple TMDB ids are found, returns the first one
    :param movie: Movie to get TMDB id for
    :return: TMDB id for the given movie
    """
    guids: List[Guid] = movie.guids
    for guid in guids:
        if guid.id.startswith("tmdb://"):
            return guid.id.split("tmdb://")[1]


def get_plex_movie_from_tmdb_id(library: LibrarySection, tmdb_movie_id: str) -> Movie:
    """
    Get a Movie object from a TMDB id
    :param library: Library section to get a Movie
    :param tmdb_movie_id:  TMDB id to get a Movie
    :return: Movie object
    """
    return library.getGuid(f"tmdb://{tmdb_movie_id}")


def get_plex_movie_from_tmdb_movie(library: LibrarySection, movie) -> Movie:
    return get_plex_movie_from_tmdb_id(library, movie["id"])


def get_plex_movies_from_tmdb_collection(
    library: LibrarySection, collection
) -> List[Movie]:
    movies: List[Movie] = []
    parts = collection.parts
    for part in parts:
        movie = get_plex_movie_from_tmdb_movie(library, part)
        movies.append(movie)

    return movies


def get_tmdb_collection_for_movie(movie):
    # Get the TMDB id for the given movie
    tmdb_id = get_tmdb_id(movie)
    logger.debug('Got TMDB ID {} for movie "{}"', tmdb_id, movie.title)
    tmdb_movie = tmdb.Movies(tmdb_id)
    tmdb_movie.info()  # make request to the TMDB api
    movie_collection_id = tmdb_movie.belongs_to_collection["id"]
    logger.debug("Acquired collection ID {}", movie_collection_id)
    # Now retrieve the collection
    collection = tmdb.Collections(movie_collection_id)
    collection.info()  # make this next request to the TMDB api
    return collection


if __name__ == "__main__":
    movie_library: LibrarySection = plex.library.section("Movies")
    movies: List[Movie] = movie_library.search("Back to the Future")
    if len(movies) == 0:
        raise Exception("No movies found")
    movie = movies[0]
    collection = get_tmdb_collection_for_movie(movie)
    plex_movies = get_plex_movies_from_tmdb_collection(movie_library, collection)
    for plex_movie in plex_movies:
        logger.debug(plex_movie.title)
    # movie_library.createCollection(collection)
    # movie_library.getGuid()
    # for media in movies:
    #     logger.debug(f"{media.title}: {get_tmdb_id(media)}")
    # tmdb_collection = tmdb.Collections(131635)
    # tmdb_collection.info()
    # tmdb_collection.results
