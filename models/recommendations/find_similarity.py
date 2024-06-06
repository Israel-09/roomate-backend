#!/usr/bin/python3
"""
find users with similarity
"""
from models.recommendations.dataframe import df
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from math import ceil


def similarity_matrix_func(df):
    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(df.drop(columns=['user_id', 'dietary_restrictions', 'hobbies']))
    similarity_matrix = cosine_similarity(normalized_features)
    return similarity_matrix

def get_top_matches(user_index, top_n=5):
    
    user_index -= 1
    similarity_matrix = similarity_matrix_func(df)
    similarity_scores = list(enumerate(similarity_matrix[user_index]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    sorted_scores = [score for score in sorted_scores if score[0] != user_index][:top_n]
    
    top_matches = [
        {
            'user_id': df.iloc[index]['user_id'],
            'compatibility': ceil(score * 100)
        }
        for index, score in sorted_scores
    ]

    return top_matches
