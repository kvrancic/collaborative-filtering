#!/usr/bin/env python3

import sys
import math
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

def read_ints():
    return list(map(int, sys.stdin.readline().strip().split()))

def compute_items_average(ratings):
    # Compute average for each item (row) ignoring missing ratings (None)
    items_avg = []
    for row in ratings:
        valid = [r for r in row if r is not None]
        avg = sum(valid) / len(valid) if valid else 0.0
        items_avg.append(avg)
    return items_avg

def compute_users_average(ratings):
    # Compute average for each user (column)
    N = len(ratings)
    M = len(ratings[0])
    users_avg = []
    for j in range(M):
        valid = [ratings[i][j] for i in range(N) if ratings[i][j] is not None]
        avg = sum(valid) / len(valid) if valid else 0.0
        users_avg.append(avg)
    return users_avg

def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

def predict_item_based(ratings, target_item, target_user, K, items_avg):
    N = len(ratings)
    # Build normalized vectors for items: subtract the item average if rating exists, otherwise use 0.
    norm = []
    for i in range(N):
        norm_row = []
        for r in ratings[i]:
            if r is not None:
                norm_row.append(r - items_avg[i])
            else:
                norm_row.append(0.0)
        norm.append(norm_row)
    
    # Compute cosine similarity between target_item and each other item.
    similarities = []
    for i in range(N):
        if i == target_item:
            # The item is identical to itself (not used later)
            continue
        sim = cosine_similarity(norm[target_item], norm[i])
        neighbor_rating = ratings[i][target_user]
        if neighbor_rating is not None:
            similarities.append((sim, neighbor_rating))
    
    # Sort neighbors by descending similarity.
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    # Take top K neighbors with positive similarity and valid rating (> 0).
    taken = 0
    numerator = 0.0
    denominator = 0.0
    for sim, r in similarities:
        if taken == K:
            break
        if sim > 0 and r > 0:
            numerator += sim * r
            denominator += sim
            taken += 1

    if denominator == 0.0:
        return 3.0  # fallback guess
    return numerator / denominator

def predict_user_based(ratings, target_item, target_user, K, users_avg):
    N = len(ratings)
    M = len(ratings[0])
    # Build transposed matrix: each row is a user’s ratings across items.
    users_matrix = []
    for j in range(M):
        user_ratings = [ratings[i][j] for i in range(N)]
        users_matrix.append(user_ratings)
    
    # Normalize each user’s vector by subtracting that user’s average.
    norm_users = []
    for j in range(M):
        norm_vec = []
        for r in users_matrix[j]:
            if r is not None:
                norm_vec.append(r - users_avg[j])
            else:
                norm_vec.append(0.0)
        norm_users.append(norm_vec)
    
    similarities = []
    # Compare target_user with every other user that has rated the target item.
    for j in range(M):
        if j == target_user:
            continue
        if users_matrix[j][target_item] is None:
            continue
        sim = cosine_similarity(norm_users[target_user], norm_users[j])
        similarities.append((sim, users_matrix[j][target_item]))
    
    similarities.sort(key=lambda x: x[0], reverse=True)
    
    taken = 0
    numerator = 0.0
    denominator = 0.0
    for sim, r in similarities:
        if taken == K:
            break
        if sim > 0:
            numerator += sim * r
            denominator += sim
            taken += 1

    if denominator == 0.0:
        return 3.0
    return numerator / denominator

def main():
    # 1) Parse initial input: N items, M users
    N, M = read_ints()

    # 2) Read the rating matrix (N lines, each with M values)
    ratings = []
    for _ in range(N):
        row = sys.stdin.readline().strip().split()
        parsed_row = [None if val == 'X' else float(val) for val in row]
        ratings.append(parsed_row)

    # Precompute averages (using only non-missing ratings)
    items_avg = compute_items_average(ratings)
    users_avg = compute_users_average(ratings)

    # 3) Number of queries Q
    Q = int(sys.stdin.readline().strip())

    # 4) Process each query
    for _ in range(Q):
        I, J, T, K = map(int, sys.stdin.readline().strip().split())
        # Convert from 1-based to 0-based indices
        I -= 1
        J -= 1

        if T == 0:
            # Item–Item CF
            predicted = predict_item_based(ratings, I, J, K, items_avg)
        else:
            # User–User CF
            predicted = predict_user_based(ratings, I, J, K, users_avg)

        # Round to 3 decimals, HALF_UP
        d = Decimal(predicted).quantize(Decimal('.001'), rounding=ROUND_HALF_UP)
        # Print with exactly 3 decimals
        print(d)

if __name__ == "__main__":
    main()
