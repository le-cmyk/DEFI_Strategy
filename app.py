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


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/ 
st.set_page_config(page_title="DEFI Projetc", page_icon=":chart_with_upwards_trend:", layout="wide")

# ---- READ CSV ----

path=r"borrow_lend_Polygon.csv"

df = get_data_from_csv(path)

# ---- SIDEBAR ----

st.sidebar.header("Please Filter Here:")

#jump_number=st.sidebar.slider("Select the project:",value=[1,4])

jump_number=2
investisment=1000
visualisation_number=10

# ---- Filtering ----



#region Creation of the returns dataframe

# ---- Creation of the project lines -----

project_lines = creation_projects_line(df)

# ---- Creation Of the list of all possible ways 

all_ways = creation_all_possible_ways(project_lines,jump_number)

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
st.subheader(f" {len(all_ways):,}")


st.markdown("""---""")

st.write(df_returns.head(1000))

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
