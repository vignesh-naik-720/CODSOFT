# -*- coding: utf-8 -*-
"""movieRatingPredictionWithPython.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SBjnXW0o5thCDlQaNf8wJpqT3CjYU71f

# **Movie Rating Prediction**
By: Vignesh Naik As part of Data Science internship at CodSoft.
"""

!pip install gradio

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import gradio as gr
import numpy as np

data = pd.read_csv("movies.csv", encoding='ISO-8859-1')

data['Year'] = data['Year'].astype(str).str.extract(r'(\d+)').astype(float).fillna(0).astype(int)
data['Votes'] = data['Votes'].astype(str).str.replace(',', '').fillna('0')
data['Votes'] = pd.to_numeric(data['Votes'], errors='coerce').fillna(0).astype(int)
data['Votes'] = np.log1p(data['Votes'])
data['Duration'] = data['Duration'].astype(str).str.extract(r'(\d+)').astype(float).fillna(0)

data = data.dropna(subset=['Rating'])
data = data.drop(columns=['Name'])

X = data.drop(columns=['Rating'])
y = data['Rating']

categorical_features = ['Genre', 'Director', 'Actor 1', 'Actor 2', 'Actor 3']
numerical_features = ['Year', 'Duration', 'Votes']

numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model.fit(X_train, y_train)

def predict_rating(year, duration, votes, genre, director, actor1, actor2, actor3):
    input_data = pd.DataFrame({
        'Year': [year],
        'Duration': [duration],
        'Votes': [votes],
        'Genre': [genre],
        'Director': [director],
        'Actor 1': [actor1],
        'Actor 2': [actor2],
        'Actor 3': [actor3]
    })

    prediction = model.predict(input_data)
    return f"The predicted rating for the movie is {prediction[0]:.2f}"

iface = gr.Interface(
    fn=predict_rating,
    inputs=[
        gr.Number(label="Year"),
        gr.Number(label="Duration (in minutes)"),
        gr.Number(label="Votes"),
        gr.Textbox(label="Genre"),
        gr.Textbox(label="Director"),
        gr.Textbox(label="Actor 1"),
        gr.Textbox(label="Actor 2"),
        gr.Textbox(label="Actor 3")
    ],
    outputs=gr.Textbox(label="Predicted Rating"),
    title="Movie Rating Predictor",
    description="Provide the details of a movie to predict its rating based on historical data. The prediction considers the movie's year, duration, votes, genre, director, and actors."
)

iface.launch()

