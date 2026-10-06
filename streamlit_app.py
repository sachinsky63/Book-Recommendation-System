import streamlit as st
import requests


st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)


API_URL = "http://127.0.0.1:8000"


st.title("📚 Book Recommendation System")

st.write(
    "Find books similar to your favorite book "
    "using collaborative filtering."
)


# Get books from FastAPI
try:

    response = requests.get(
        f"{API_URL}/books"
    )

    response.raise_for_status()

    books = response.json()["books"]

except requests.exceptions.ConnectionError:

    st.error(
        "FastAPI server is not running. "
        "Start FastAPI first."
    )

    st.stop()


# Book selection
selected_book = st.selectbox(
    "Select a book",
    books
)


# Recommendation
if st.button("✨ Recommend Books"):

    response = requests.get(
        f"{API_URL}/recommend",
        params={
            "book_name": selected_book
        }
    )


    if response.status_code == 200:

        data = response.json()

        recommendations = data["recommendations"]


        if recommendations:

            st.subheader(
                f"Recommended books for: {selected_book}"
            )


            columns = st.columns(5)


            for col, book in zip(
                columns,
                recommendations
            ):

                with col:

                    try:

                        st.image(
                            book["image"],
                            width=150
                        )

                    except Exception:

                        st.write("📕")


                    st.write(
                        f"**{book['title']}**"
                    )

                    st.caption(
                        book["author"]
                    )

        else:

            st.warning(
                "No recommendations found."
            )

    else:

        st.error(
            "Something went wrong with the API."
        )