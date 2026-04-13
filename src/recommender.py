from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV of songs and return a list of dicts with correctly typed fields."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded {len(songs)} songs.")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences using categorical bonuses and Gaussian proximity; return (score, reasons)."""
    import math

    score = 0.0
    reasons = []

    # Categorical matches (max 2.25)
    if song["genre"] == user_prefs.get("favorite_genre"):
        score += 1.5
        reasons.append(f"genre match (+1.5)")

    if song["mood"] == user_prefs.get("favorite_mood"):
        score += 0.75
        reasons.append(f"mood match (+0.75)")

    # Gaussian proximity: exp(-5 * (song_value - target)^2) (max 4.75)
    def gaussian(song_val: float, target: float) -> float:
        return math.exp(-5 * (song_val - target) ** 2)

    numerical = [
        ("energy",       "target_energy",       2.0),
        ("valence",      "target_valence",       1.0),
        ("danceability", "target_danceability",  0.9),
        ("acousticness", "target_acousticness",  0.85),
    ]

    for feature, pref_key, weight in numerical:
        if pref_key in user_prefs:
            raw = gaussian(song[feature], user_prefs[pref_key])
            points = raw * weight
            score += points
            reasons.append(f"{feature} proximity ({points:+.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
