# to run the app : streamlit run app.py
# to have the correct version  : pipreqs --encoding=utf8 --force


import streamlit as st  # pip install streamlit
import bisect
import json


#---- Importation of the class and functions

from Functions.Essential_for_ProjectLine import get_data_from_csv
from Functions.Ways_retruns import creation_projects_line, creation_all_possible_ways ,json_return ,creation_sorted_json
from Functions.Filtre import get_unique_crypto_values, exclude_crypto
from Functions.plots import differents_returns

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/ 
st.set_page_config(page_title="DEFI Project", page_icon=":chart_with_upwards_trend:", layout="wide")

# ---- READ CSV ----

path=r"borrow_lend_Polygon.csv"

df = get_data_from_csv(path)

# ---- SIDEBAR ----

#region SIDEBAR

#For exponnential options in the sidebar
def create_options(n, min, max, value):
  result = []
  # Calculate the base of the exponential function
  base = (max / min) ** (1 / (n - 1))
  for i in range(n):
    result.append(round(min * base ** i))
  
  # Check if the value is in the result list
  if value not in result:
    # Find the closest index to insert the value
    index = bisect.bisect_left(result, value)
    # Insert the value at that index
    result.insert(index, value)
  
  return result

st.sidebar.header("Please Filter Here:")

jump_number=st.sidebar.slider("Select the number project visited :",
                              min_value = 1, 
                              max_value = 4, 
                              value = 2)

investisment=st.sidebar.slider("Select the investment amount :",
                               min_value = 1, 
                               max_value = 10000, 
                               value = 1000)


selected_duration = st.sidebar.slider("Select the duration in year :",
                            min_value=float(0),
                            max_value=float(2),
                            value=float(1))

list_exclude_crypto = st.sidebar.multiselect("Select the Crypto to exclued",
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

#endregion


# ---- Filtering ----

df_selection=exclude_crypto(df, list_exclude_crypto)

#region Creation of the returns dataframe

# ---- Creation of the project lines -----

project_lines = creation_projects_line(df_selection)

# ---- Creation Of the list of all possible ways 

all_ways = creation_all_possible_ways(project_lines,jump_number,crypto_to_begin,crypto_to_finish)

# ---- Creation of a list of dictionnary for all returns

Json_Return=json_return(all_ways,investisment,selected_duration)

# ---- Creation of the Json for all returns



number_of_all_ways=len(all_ways)

# Display a select slider with the options

options=create_options(70, 1, number_of_all_ways,10)
visualisation_number = st.sidebar.select_slider('Select the visualisation number :', 
                                                options=options,
                                                value=10)



Json_Return_sorted=creation_sorted_json(Json_Return,visualisation_number)

#endregion

# ---- MAINPAGE ----
st.title(":bar_chart: Defi Projet")
st.markdown("##")


# ----TOP KPI's
c_1, c_2,c_3 = st.columns(3)
with c_1:
    st.subheader("Number of possible ways:")
    st.subheader(f" {number_of_all_ways:,}")
with c_2:
    st.subheader("Best way:")
    best_element=Json_Return_sorted["ways"][0]

    for element in best_element["way"]:
        string_value=f"{element['Project']} : {element['Borrow']} → {element['Lend']}"
        st.write(string_value)
with c_3:
    st.subheader("Best return:")
    st.subheader(f" {round(best_element['return'],2):,}")

st.markdown("""---""")


#----- Visualisations and DATA


tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

#---- Plot different return

tab1.write(differents_returns(Json_Return_sorted,investisment))

#---- Enable to download the data

tab2.download_button(
    label="Download data as JSON",
    data=json.dumps(Json_Return_sorted),
    file_name='land_borrow.json',
    mime='text/json',
)

#---- Visualisation of the data brut

tab2.write(Json_Return_sorted)




#---- test




#---- Link and Sources

link = '[GitHub](https://github.com/le-cmyk/DEFI_Strategy)'

c_1, c_2,c_3 = st.columns(3)

with c_2:
    st.markdown(link, unsafe_allow_html=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
