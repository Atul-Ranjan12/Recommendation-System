from PopularityRecommender import PopularityRecommender
from helpers import get_article_attributes
import streamlit as st
import pandas as pd
from PIL import Image

# Set up dataframes
article_df = pd.read_csv("./articles.csv")

st.set_page_config(
    page_title="Home",
    page_icon="🏠"
)

# Set up recommenders
if "popularity_recommendations" not in st.session_state:
    popularity_recommender = PopularityRecommender()
    st.session_state["popularity_recommendations"] = popularity_recommender.recommend(100)

if "user_product_cart" not in st.session_state:
    st.session_state['user_product_cart'] = []

# Style for streamlit button
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(204, 49, 49);
    color: white;
}
</style>""", unsafe_allow_html=True)


def show_one_article(article_id, key):
    props = get_article_attributes(article_id, article_df)
    image = Image.open(props["image_path"])
    c1, c2 = st.columns(2)
    with c1:
        st.image(image)
    with c2:
        st.write(f"## {props['name']}")
        st.markdown(f"""##### {props['section']}, {props['attributes']}""")
        st.write(props['description'][:100])

        add_to_cart_button = st.button("Add to Cart!", key=key)
        if add_to_cart_button:
            arr = st.session_state['user_product_cart']
            arr.append(key)
            st.session_state['user_product_cart'] = arr

    st.markdown("""<br>""", unsafe_allow_html=True)
    st.markdown("""<hr /> """, unsafe_allow_html=True)
    st.markdown("""<br>""", unsafe_allow_html=True)


def show_popular_articles(j):
    for article in st.session_state["popularity_recommendations"][:j]:
        show_one_article(article, article)


def show_cart():
    st.write("## Your Cart")
    cart_products = st.session_state['user_product_cart']
    counter = 1
    for prod in cart_products:
        prod_attr = get_article_attributes(prod, article_df)
        image = Image.open(prod_attr["image_path"])
        image64 = image.resize((64, 64))
        c1, c2 = st.columns(2)
        with c1:
            st.image(image64)
        with c2:
            st.write(prod_attr["name"])
        col1, col2, col3 = st.columns(3)
        with col2:
            remove_prod_key = st.button("Delete", key=f"remCart{counter}")
            if remove_prod_key:
                remove_product_from_cart(prod)
        counter += 1
        st.markdown("""<hr /> """, unsafe_allow_html=True)


def remove_product_from_cart(id):
    arr = st.session_state["user_product_cart"]
    arr.remove(id)
    st.session_state["user_product_cart"] = arr


st.write("# Our Most Popular Products \n\n")

options = [15, 25, 50, 100]
selection = st.selectbox("Choose number of articles to be viewed", options)
show_popular_articles(selection)

with st.sidebar:
    show_cart()


