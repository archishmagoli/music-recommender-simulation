# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
