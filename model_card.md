# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

VibeFinder suggests songs from a small catalog based on a user's stated taste profile. It is built for classroom exploration — not for real users or real music services.

It assumes the user already knows their preferences and can describe them upfront (favorite genre, mood, energy level, etc.). It should not be used to recommend music to people who haven't provided explicit preferences, and it should not be treated as a substitute for a production recommender system.

---

## 3. How the Model Works  

Every song in the catalog gets a score based on how closely it matches the user's taste profile. The score has two parts.

First, the system checks for exact label matches. If the song's genre matches the user's favorite genre, it gets bonus points. Same for mood. These are simple yes/no checks.

Second, for numerical features — energy, valence, danceability, and acousticness — the system measures how close the song's value is to the user's target. A song that lands right on the target scores full points. A song that's far off scores close to zero. The scoring uses a bell curve shape, so being slightly off costs a little, but being way off costs a lot.

All the individual scores are added up, every song is ranked highest to lowest, and the top 5 are returned as recommendations with a plain-English explanation of what drove the score.

---

## 4. Data  

The catalog has 18 songs, hand-curated for this simulation. It covers 15 genres (pop, lo-fi, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b, classical, country, metal, folk, edm, blues) and 14 moods (happy, chill, intense, relaxed, moody, focused, upbeat, romantic, peaceful, nostalgic, angry, melancholic, euphoric, sad).

Each song has 5 numerical features — energy, valence, danceability, acousticness, and tempo — all on a 0 to 1 scale. There are no lyrics, no release dates, no cultural context, and no audio files. The model only sees numbers.

Lo-fi is over-represented with 3 songs. Most other genres have exactly 1. The catalog does not reflect the full diversity of music taste — it leans toward Western genres and does not include classical Indian, Latin, African, or other global styles.

---

## 5. Strengths  

The system works best for users with clear, consistent preferences. If someone wants high-energy pop or chill lo-fi, the top result is an obvious match and the rankings feel intuitive.

The bell curve scoring is a strength — a song that's slightly off still gets partial credit instead of being completely ignored. This means the top 5 list has gradual variation rather than a sharp cliff between results.

The explanation output is transparent. Every recommendation comes with a reason like "genre match (+1.5), energy proximity (+1.98)" so it's always clear why a song ranked where it did. That kind of explainability is something real systems like Spotify rarely surface to users.

---

## 6. Limitations and Bias 

The clearest weakness discovered through testing is **catalog density skew**. Lo-fi makes up 3 of 18 songs in the dataset, and when we ran the Chill Lo-fi profile, all three lo-fi songs occupied the top three spots — Library Rain, Midnight Coding, and Focus Flow — with scores of 6.97, 6.95, and 6.24 respectively. The gap between #3 and #4 (Spacewalk Thoughts at 5.17) was nearly a full point, meaning a user gets the same genre recommended back to them repeatedly just because the catalog happens to have more of it. In a real system with hundreds of genres, this kind of density imbalance would create a filter bubble where certain genres dominate recommendations not because they fit the user best, but because the dataset over-represents them.

---

## 7. Evaluation  

We tested three user profiles — **High-Energy Pop**, **Chill Lo-fi**, and **Deep Intense Rock** — and manually checked whether the top 5 results felt like songs that person would actually want to hear.

For all three, the #1 result was a near-perfect match: Gym Hero for the pop listener, Library Rain for the lo-fi listener, Storm Runner for the rock listener. These results matched our intuition, which gave us confidence the scoring logic was working as intended.

What was more surprising was the behavior just below the top result. For the **High-Energy Pop** profile, Sunrise City ranked #2 even though its mood is "happy" and the profile asked for "intense." The reason is simple once you see it: Sunrise City is still a pop song with high energy, so it picks up the genre bonus and scores well on energy and danceability — the one missing piece (mood) only costs 0.75 points out of 7.00. To a non-programmer, this looks like the system saying "I know you said intense, but this happy pop song sounds so similar that it's basically the same." That is a reasonable call in practice, but it shows that mood matters less than the numerical features when they line up strongly.

For the **Deep Intense Rock** profile, Iron Cathedral (metal) and Night Drive Loop (synthwave) scored almost identically — 4.38 vs 4.41 — even though they sound nothing alike. The reason is that their energy, danceability, and acousticness values happen to be numerically close to the rock profile's targets. The system has no concept of what "rock" actually sounds like; it only sees numbers. This was the most informative finding: a content-based recommender can be fooled by numeric coincidence when the catalog is small.

For a detailed comparison of how each pair of profiles differed in their outputs, see [reflection.md](reflection.md).

---

## 8. Future Work  

- **Mood and genre similarity:** Instead of exact string matching, group related labels together. "Happy" and "upbeat" should be considered close, and "pop" and "indie pop" should share partial credit.
- **Diversity cap:** Add a rule that prevents more than 2 songs from the same genre appearing in the top 5, so results don't collapse into a single genre just because the catalog has more of it.
- **Feedback loop:** Let the profile update based on what the user actually plays. If a song gets skipped, reduce the weight for features it had. If a song gets replayed, boost them. Right now the system recommends the same 5 songs every single time.

---

## 9. Personal Reflection  

The biggest learning moment for me in the project was designing the weighted scoring logic. Seeing how assigning different point values to genre, mood, and energy actually shifted which songs surfaced — and why — made the whole idea of a "scoring rule" concrete in a way that just reading about it wouldn't have. Watching the weights get rebalanced after the adversarial profiles exposed the genre-over-prioritization problem was a good reminder that even small numbers carry real consequences.

Using AI tools throughout this project changed how I think about the search process itself. It wasn't just about finding answers faster — it was about figuring out what to search for and how to frame the problem in the first place. That kind of intent-based assistance made it easier to go from a vague idea ("songs that feel similar") to a specific implementation (Gaussian proximity on normalized features).

What surprised me most was how much the system felt like real recommendations even with only 18 songs and a handful of math operations. The results weren't random; they had reasons, and those reasons made sense. It was a good reminder that a lot of what feels "intelligent" in consumer apps to me might be simpler under the hood than it appears.

If I extended this project, the first thing I'd do is test it against a much larger dataset — hundreds or thousands of songs — to see whether the scoring logic actually holds up or whether it only worked because the catalog was small enough to tune by hand.
