# to run the app : streamlit run app.py
# to have the correct version  : pipreqs --encoding=utf8 --force



import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit
import folium
from streamlit_folium import folium_static

#---- Importation of the class and functions

from Functions.Essential_for_ProjectLine import get_data_from_csv
from Functions.Ways_retruns import creation_projects_line, creation_all_possible_ways ,creation_all_returns,creation_sorted_df_retruns
from Functions.Filtre import get_unique_crypto_values, exclude_crypto

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/ 
st.set_page_config(page_title="DEFI Projetc", page_icon=":chart_with_upwards_trend:", layout="wide")

# ---- READ CSV ----

path=r"borrow_lend_Polygon.csv"

df = get_data_from_csv(path)

# ---- SIDEBAR ----

st.sidebar.header("Please Filter Here:")

jump_number=st.sidebar.slider("Select the number project visited :",
                              min_value = 1, 
                              max_value = 4, 
                              value = 2)

investisment=st.sidebar.slider("Select the investment amount :",
                               min_value = 1, 
                               max_value = 10000, 
                               value = 1000)

list_exclude_crypto = st.sidebar.multiselect("Select the Crypto to exclued:",
                                             options=get_unique_crypto_values(df),
                                             default=['LINK'])

crypto_to_begin=st.sidebar.selectbox("Select the begining crypto", 
                 get_unique_crypto_values(df,list_exclude_crypto,1),
                 disabled=False, 
                 label_visibility="visible")

crypto_to_finish=st.sidebar.selectbox("Select the last crypto", 
                 get_unique_crypto_values(df,list_exclude_crypto,2),
                 disabled=False, 
                 label_visibility="visible")

# ---- Filtering ----

df_selection=exclude_crypto(df, list_exclude_crypto)

#region Creation of the returns dataframe

# ---- Creation of the project lines -----

project_lines = creation_projects_line(df_selection)

# ---- Creation Of the list of all possible ways 

all_ways = creation_all_possible_ways(project_lines,jump_number,crypto_to_begin,crypto_to_finish)

# ---- Creation of a list of dictionnary for all returns

returns = creation_all_returns(all_ways,investisment)

# ---- Creation of the dataframe for all returns

df_returns = creation_sorted_df_retruns(returns)

#endregion

# ---- MAINPAGE ----
st.title(":bar_chart: Defi Projet")
st.markdown("##")

# ----TOP KPI's

st.subheader("Number of possible ways:")
number_of_all_ways=len(all_ways)
st.subheader(f" {number_of_all_ways:,}")


st.markdown("""---""")

#---- Number of visualized data

visualisation_number=st.sidebar.slider("Select the visualisation number :",
                                       min_value = 1, 
                                       max_value = number_of_all_ways, 
                                       value = 10 )

st.write(df_returns.head(visualisation_number))

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
