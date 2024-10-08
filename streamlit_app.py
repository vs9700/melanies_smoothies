# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your Custom Smoothie!
    """
)
name_on_the_order=st.text_input('Name on Smoothie:')
st.write('The name on the smoothie will be:',name_on_the_order)
cnx = st.connection("snowflake")
session= cnx.session()
my_data_frame =session.table('smoothies.public.fruit_options').select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_data_frame, use_container_width=True)
#st.stop()
# converting snowpark data frame to pandas
pd_df = my_data_frame.to_pandas()
#st.dataframe(pd_df)
#st.stop()
ingrediant_list=st.multiselect('choose up to 5 ingrediants',my_data_frame,max_selections=5)
if ingrediant_list:
    #st.write(ingrediant_list)
   # st.text(ingrediant_list)
    ingrediant_string =''
    for fruit_choosen in ingrediant_list:
        ingrediant_string += fruit_choosen+ ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_choosen,' is ', search_on, '.')
        st.subheader(fruit_choosen+" Nutrition Information")
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width =True)

    #st.write(ingrediant_string)
    my_insert_stmt= """insert into smoothies.public.orders(ingredients,name_on_order)
    values('"""+ingrediant_string+"""','"""+name_on_the_order+"""')"""
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your smoothie is ordered, "+ name_on_the_order+'!', icon="✅")

