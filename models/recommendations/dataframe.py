#!/usr/bin/python3
"""
process the preference table to dataframe
"""
from models.engine.database import DB
import pandas as pd


db = DB()
preferences = db.all_user_preference()
preferences_list = []

def map_preferences(df):
    mappings = {
        'cleanliness': {'Low': 1, 'Medium': 2, 'High': 3},
        'noise_tolerance': {'Low': 1, 'Medium': 2, 'High': 3},
        'sleep_schedule': {'Irregular': 1, 'Regular': 2, 'Late': 3},
        'study_habits': {'Quiet': 1, 'Active': 2, 'Intense': 3, 'Focused': 4},
        'social_habits': {'Few close friends': 1, 'Moderate': 2, 'Very social': 3},
        'smoking': {'No': 0, 'Yes': 1},
        'comfort_with_cultural_diversity': {'Somewhat comfortable': 1, 'Comfortable': 2, 'Very comfortable': 3},
        'willingness_to_share_expenses': {False: 0, True: 1},
    }
    
    for column, mapping in mappings.items():
        df[column] = df[column].map(mapping)
    
    return df


for pref in preferences:
    preferences_list.append({
        'user_id': pref.user_id,
        'cleanliness': pref.cleanliness,
        'noise_tolerance': pref.noise_tolerance,
        'sleep_schedule': pref.sleep_schedule,
        'study_habits': pref.study_habits,
        'social_habits': pref.social_habits,
        'smoking': pref.smoking,
        'dietary_restrictions': pref.dietary_restrictions,
        'hobbies': pref.hobbies,
        'comfort_with_cultural_diversity': pref.comfort_with_cultural_diversity,
        'willingness_to_share_expenses': pref.willingness_to_share_expenses,
    })

df = pd.DataFrame(preferences_list)
df = map_preferences(df)
