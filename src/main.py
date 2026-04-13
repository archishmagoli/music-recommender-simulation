"""
Command line runner for the Music Recommender Simulation.
Runs multiple user profiles — including adversarial edge cases — to evaluate scoring behavior.
"""

import os
from .recommender import load_songs, recommend_songs

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

PROFILES = [
    # --- Standard profiles ---
    (
        "High-Energy Pop",
        {
            "favorite_genre":      "pop",
            "favorite_mood":       "intense",
            "target_energy":       0.92,
            "target_valence":      0.78,
            "target_danceability": 0.88,
            "target_acousticness": 0.05,
        },
    ),
    (
        "Chill Lofi",
        {
            "favorite_genre":      "lofi",
            "favorite_mood":       "chill",
            "target_energy":       0.38,
            "target_valence":      0.58,
            "target_danceability": 0.60,
            "target_acousticness": 0.80,
        },
    ),
    (
        "Deep Intense Rock",
        {
            "favorite_genre":      "rock",
            "favorite_mood":       "intense",
            "target_energy":       0.91,
            "target_valence":      0.45,
            "target_danceability": 0.65,
            "target_acousticness": 0.10,
        },
    ),
    # --- Adversarial / edge case profiles ---
    (
        "Conflicting: High Energy + Sad Mood",
        {
            "favorite_genre":      "blues",
            "favorite_mood":       "sad",
            "target_energy":       0.90,   # high energy...
            "target_valence":      0.20,   # ...but very low valence (dark/sad)
            "target_danceability": 0.55,
            "target_acousticness": 0.50,
        },
    ),
    (
        "The Neutralist: Everything at 0.5",
        {
            "favorite_genre":      "",     # no genre preference
            "favorite_mood":       "",     # no mood preference
            "target_energy":       0.50,
            "target_valence":      0.50,
            "target_danceability": 0.50,
            "target_acousticness": 0.50,
        },
    ),
    (
        "Acoustic but Intense",
        {
            "favorite_genre":      "folk",
            "favorite_mood":       "angry",
            "target_energy":       0.95,   # wants high energy...
            "target_valence":      0.30,
            "target_danceability": 0.50,
            "target_acousticness": 0.90,   # ...but also very acoustic (rarely co-occur)
        },
    ),
]


def run_profile(label: str, user_prefs: dict, songs: list) -> None:
    print("\n" + "=" * 54)
    print(f"  Profile: {label}")
    print("=" * 54)
    recommendations = recommend_songs(user_prefs, songs, k=5)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{i}  {song['title']}  -  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"       Score: {score:.2f} / 7.00  (categorical max 2.25, numerical max 4.75)")
        print(f"       Why:   {explanation}")
    print()


def main() -> None:
    songs = load_songs(DATA_PATH)
    for label, prefs in PROFILES:
        run_profile(label, prefs, songs)


if __name__ == "__main__":
    main()
