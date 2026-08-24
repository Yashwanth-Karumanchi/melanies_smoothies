import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")

my_dataframe = cnx.query(
    """
    SELECT FRUIT_NAME
    FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS
    """
)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe["FRUIT_NAME"],
    max_selections=5
)

if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        cnx.query(
            f"""
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS
            (INGREDIENTS, NAME_ON_ORDER)
            VALUES ('{ingredients_string}', '{name_on_order}')
            """
        )

        st.success(
            "Your Smoothie is ordered, " + name_on_order + "!",
            icon="✅"
        )
