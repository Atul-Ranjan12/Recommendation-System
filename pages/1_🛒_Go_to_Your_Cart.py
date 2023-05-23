import pandas as pd
import streamlit as st
from helpers import get_article_attributes
from PIL import Image

from ContentBasedRecommender import ContentBasedRecommender
from UserSimilarityRecommender import UserSimilarityRecommender

# Set up dataframes
article_df = pd.read_csv("././articles.csv")

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(204, 49, 49);
    color: white;
    width: 100%;
}
</style>""", unsafe_allow_html=True)

# Initialize recommenders
item_sim_recommender = ContentBasedRecommender()
user_sim_recommender = UserSimilarityRecommender()

# Fetch Recommendations and store on session
if "item_sim_recs" not in st.session_state:
    recs = []
    for item in st.session_state["user_product_cart"]:
        sim_items = item_sim_recommender.get_recommendations(item, 3)
        recs.append(sim_items)
    st.session_state["item_sim_recs"] = recs

if "user_sim_recs" not in st.session_state:
    st.session_state["user_sim_recs"] = user_sim_recommender.recommend_new_user(st.session_state["user_product_cart"], 5)


st.write("# Your Cart")


def show_one_article(article_id):
    props = get_article_attributes(article_id, article_df)
    image = Image.open(props["image_path"])
    c1, c2 = st.columns(2)
    with c1:
        st.image(image)
    with c2:
        st.write(f"## {props['name']}")
        st.markdown(f"""##### {props['section']}, {props['attributes']}""")
        st.write(props['description'][:100])


def show_cart_items():
    counter = 0
    for i, article in enumerate(st.session_state["user_product_cart"]):
        show_one_article(article)
        rec_items = st.session_state["item_sim_recs"][i]
        st.write("## Similar Products to your Choice: ")
        col1, col2, col3 = st.columns(3)
        with col1:
            item1 = rec_items[0]
            item_attrs = get_article_attributes(item1, article_df)
            image1 = Image.open(item_attrs["image_path"])
            fin_image1 = image1.resize((128, 128))
            st.image(fin_image1)
            st.write(f"##### {item_attrs['name']}")
            st.markdown(f"""{item_attrs['section']}, {item_attrs['attributes']}""")
        with col2:
            item2 = rec_items[1]
            item_attrs2 = get_article_attributes(item2, article_df)
            image2 = Image.open(item_attrs2["image_path"])
            fin_image2 = image2.resize((128, 128))
            st.image(fin_image2)
            st.write(f"##### {item_attrs2['name']}")
            st.markdown(f"""{item_attrs2['section']}, {item_attrs2['attributes']}""")
        with col3:
            item3 = rec_items[2]
            item_attrs3 = get_article_attributes(item3, article_df)
            image3 = Image.open(item_attrs3["image_path"])
            fin_image3 = image3.resize((128, 128))
            st.image(fin_image3)
            st.write(f"##### {item_attrs3['name']}")
            st.markdown(f"""{item_attrs3['section']}, {item_attrs3['attributes']}""")
        counter += 1

        st.markdown("""<br>""", unsafe_allow_html=True)
        st.markdown("""<hr /> """, unsafe_allow_html=True)
        st.markdown("""<br>""", unsafe_allow_html=True)


def show_user_sim_items():
    for item_id in st.session_state["user_sim_recs"]:
        show_one_article(item_id)

        st.markdown("""<br>""", unsafe_allow_html=True)
        st.markdown("""<hr /> """, unsafe_allow_html=True)
        st.markdown("""<br>""", unsafe_allow_html=True)


show_cart_items()
st.write("#### Confirm your Checkout:")
checkout_button = st.button("Proceed to checkout", key="checkoutButton")

st.write("# Users like you also pick:")
show_user_sim_items()
