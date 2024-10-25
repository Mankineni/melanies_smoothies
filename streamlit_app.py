# Import python packages
import streamlit as st
cnx = st.connections("snow_flake")
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title('Customize your Smoothie :cup_with_straw:')
st.write(
    """Choose the fruits you want in your custome Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The Name on Your Smoothie Will Be: ',name_on_order)

session = cnx.session()    
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5)

#st.write(ingredients_list)
#st.text(ingredients_list)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)
    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order) 
                    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is Ordered, '+ name_on_order+"""!""", icon="✅")
