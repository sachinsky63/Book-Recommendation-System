from fastapi import FastAPI
import pickle
import numpy as np


app = FastAPI(
    title="Book Recommendation API",
    description="Collaborative Filtering Based Book Recommendation System",
    version="1.0"
)


# Load data
books = pickle.load(open("books.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
similarity_scores = pickle.load(
    open("similarity_scores.pkl", "rb")
)


def recommend(book_name):

    if book_name not in pt.index:
        return []

    index = np.where(
        pt.index == book_name
    )[0][0]

    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommendations = []

    for i in similar_items:

        title = pt.index[i[0]]

        book_data = books[
            books["Book-Title"] == title
        ].drop_duplicates("Book-Title")

        if len(book_data) > 0:

            row = book_data.iloc[0]

            recommendations.append({
                "title": row["Book-Title"],
                "author": row["Book-Author"],
                "image": row["Image-URL-M"]
            })

    return recommendations


# Home
@app.get("/")
def home():

    return {
        "message": "Book Recommendation API is running"
    }


# Get all books
@app.get("/books")
def get_books():

    return {
        "books": list(pt.index)
    }


# Recommendation API
@app.get("/recommend")
def get_recommendations(book_name: str):

    recommendations = recommend(book_name)

    return {
        "book": book_name,
        "recommendations": recommendations
    }