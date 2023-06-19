
import streamlit
import requests
import pandas
import snowflake.connector

from urllib.error import URLError
streamlit.title('My parents new healthy diner')
streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)
def get_fruity_vice(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
streamlit.header("Fruityvice Fruit Advice!")
try:
  
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error('Please select a fruit to get information')
      #streamlit.write('The user entered ', fruit_choice)
   else:
      back_from_function=get_fruity_vice(fruit_choice)
           
      # write your own comment - what does this do?
      streamlit.dataframe(back_from_function)
#
except URLError as e:
  streamlit.error()
#streamlit.stop()  

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
#my_data_row = my_cur.fetchall()
streamlit.header("fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
    return my_cur.fetchall()
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows=get_fruit_load_list()
  #my_cur = my_cnx.cursor()
  streamlit.dataframe(my_data_rows)
#streamlit.header("next fruit you want to add :")
#add_my_fruit= streamlit.text_input('next fruit you want to add : ?','Jackfruit')
#streamlit.write('The user entered ', add_my_fruit)
#my_cur.execute("insert into FRUIT_LOAD_LIST values('from ')")
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into FRUIT_LOAD_LIST values('" +????+ "')")
    return 'thanks for adding ' + new_fruit
add_my_fruit= streamlit.text_input('next fruit you want to add : ?')
if streamlit.button('add a fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function=insert_row_snowflake(add_my_fruit)
  streamlit.text('back from function')
  
