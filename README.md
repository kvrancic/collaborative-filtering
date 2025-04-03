# Collaborative Filtering (Item–Item & User–User)

This repository contains an implementation of collaborative filtering for a recommender system, using **item–item** and **user–user** approaches. It was created for the *Mining Massive Data Sets / Analiza velikih skupova podataka* course assignment.

## Overview

- **Item–Item CF**  
  Predicts a missing rating by looking at similar items and the user’s known ratings on them.

- **User–User CF**  
  Predicts a missing rating by looking at similar users and the items they have rated.

- **Similarity Metric**  
  (Describe whichever metric you used, e.g., cosine similarity or Pearson correlation.)

## How It Works

1. **Input**  
   - First line: Two integers, `N` (items) and `M` (users).  
   - Next `N` lines: User–item matrix with integers (1–5) or `'X'` for missing entries.  
   - Next line: Integer `Q` for the number of queries.  
   - Next `Q` lines: Each query is `I J T K`:
     - `I` → target item index (1–N)  
     - `J` → target user index (1–M)  
     - `T` → 0 for item–item, 1 for user–user CF  
     - `K` → maximum number of neighbors to consider  

2. **Processing**  
   - Compute similarities only for items/users that have valid ratings where needed.  
   - Filter out items/users with non-positive similarity.  
   - Select up to `K` neighbors with the highest similarity.  
   - Take a weighted average of the ratings from these neighbors (weighted by similarity).

3. **Output**  
   - For each query, print the predicted rating with exactly three decimal places, rounded in *HALF_UP* mode.  
   - Example: `3.000`

## Usage

1. **Build/Install**  
   - Just run `python CF.py < input_file > output_file`.  
2. **Check Example**  
   - A sample input and expected output are provided for testing. Compare your output to the official solution to validate.

