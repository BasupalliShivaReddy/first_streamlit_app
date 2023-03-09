import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('New Healthy Breakfast')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# reading csv file using pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
#Selecting only fruits from the list to display
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)










#Frutyvice test

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+str(this_fruit_choice))
  # streamlit.text(fruityvice_response.json()) #just writes dat to the screen
  # Normalizing the json  
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")  
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(this_fruit_choice)
    streamlit.dataframe(back_from_function)
    streamlit.write('The user entered ', fruit_choice)
    
except URLError as e:
  streamlit.error()


#streamlit.stop()

streamlit.header("The Fruit Load List Contains:") 
def get_fruitload_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
  
# Add abutton to load the fruits
if streamlit.button('Great Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruitload_list()
  streamlit.dataframe(my_data_rows)
  
  
# Allowing user to add a fruit
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT into fruit_load_list values ('"+ new_fruit +"'))")
    return "Thanks for adding "+ new_fruit
  
fruit_add = streamlit.text_input("What fruit would you like to add") 
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_funtion1 = insert_row_snowflake(fruit_add)
  streamlit.text(back_from_funtion1)
  
