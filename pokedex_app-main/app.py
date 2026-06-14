import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import streamlit as st

web_url = "https://pokemondb.net/pokedex/all"
raw_content = requests.get(web_url)

parsed_content = bs(raw_content.text, "html.parser")

table = parsed_content.find("table", id="pokedex")

table_body = table.tbody

list_of_rows = table_body.find_all("tr")

pokedex = list()
for row in list_of_rows:
    stats = dict()
    name_row = row.find("td", class_="cell-name")
    stats['name'] = name_row.a.text
    num_rows = row.find_all("td", class_="cell-num")
    stats['total'] = num_rows[1].text
    stats['HP'] = num_rows[2].text
    stats['phAtk'] = num_rows[3].text
    stats['phDef'] = num_rows[4].text
    stats['spAtk'] = num_rows[5].text
    stats['spDef'] = num_rows[6].text
    stats['speed'] = num_rows[7].text
    pokedex.append(stats)
pokedex_df = pd.DataFrame(pokedex)

st.sidebar.title("Search for a pokemon")
filter = st.sidebar.selectbox("Pokemon", ["All"] + list(pokedex_df["name"].unique()) )

st.title("PokedexApp")
if(filter == "All"):
    filtered_df = pokedex_df
else:
    filtered_df = pokedex_df[pokedex_df["name"] == filter]
st.write(filtered_df)

