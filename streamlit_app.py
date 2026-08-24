import streamlit as st

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")

my_dataframe = cnx.query(
    """
    SELECT FRUIT_NAME
    FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS
    """,
    ttl=0
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
        cursor = cnx.cursor()
    
        cursor.execute(
            """
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS
            (INGREDIENTS, NAME_ON_ORDER)
            VALUES (?, ?)
            """,
            [ingredients_string, name_on_order]
        )
    
        st.success(
            "Your Smoothie is ordered, " + name_on_order + "!",
            icon="✅"
        )

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
