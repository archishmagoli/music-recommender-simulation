"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
from .recommender import load_songs, recommend_songs

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


def main() -> None:
    songs = load_songs(DATA_PATH)

    user_prefs = {
        "favorite_genre":     "indie pop",
        "favorite_mood":      "happy",
        "target_energy":      0.72,
        "target_valence":     0.75,
        "target_danceability": 0.76,
        "target_acousticness": 0.30,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  Top Recommendations")
    print("=" * 50)

    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']}  -  {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 7.00")
        print(f"    Why:   {explanation}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
