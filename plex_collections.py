#  Copyright (c) 2023 Edgeburn Media. All rights reserved.
import os

import tmdbsimple as tmdb
from plexapi.server import PlexServer

# TMDB
tmdb.API_KEY = os.environ.get("TMDB_API_KEY")

# Plex
plex_base_url = os.environ.get("PLEX_BASE_URL")
plex_api_key = os.environ.get("PLEX_API_KEY")
plex = PlexServer(plex_base_url, plex_api_key)


if __name__ == "__main__":
    pass
