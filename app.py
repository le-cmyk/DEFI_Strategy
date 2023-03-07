# to run the app : streamlit run app.py
# to have the correct version  : pipreqs --encoding=utf8 --force



import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit
import folium
from streamlit_folium import folium_static
import re

#---- Importation of the class and functions

from Functions.Essential_for_ProjectLine import get_data_from_csv
from Functions.Ways_retruns import creation_projects_line, creation_all_possible_ways ,json_return ,creation_sorted_json
from Functions.Filtre import get_unique_crypto_values, exclude_crypto

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/ 
st.set_page_config(page_title="DEFI Project", page_icon=":chart_with_upwards_trend:", layout="wide")

# ---- READ CSV ----

path=r"borrow_lend_Polygon.csv"

df = get_data_from_csv(path)

# ---- SIDEBAR ----

#region SIDEBAR
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

visualisation_number=st.sidebar.slider("Select the visualisation number :",
                                       min_value = 1, 
                                       max_value = number_of_all_ways, 
                                       value = 10 )



Json_Return_sorted=creation_sorted_json(Json_Return,visualisation_number)

#endregion

# ---- MAINPAGE ----
st.title(":bar_chart: Defi Projet")
st.markdown("##")

#---- Get a value in a string

def get_value(string,to_find):
  pattern = f"{to_find}: (\w+)"
  match = re.search(pattern, string)
  if match:
    return match.group(1)
  else:
    return None

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


def differents_returns(json_file,investisment):
    returns = []
    ways = []
    labels, labels2= [],[]
    investisment_pourcentage=[]
    for i in range(len(json_file["ways"])):
        returns.append(json_file["ways"][i]["return"])
        ways.append(str(i+1))
        labels.append(f"Best way n°{i+1}")
        investisment_pourcentage.append(json_file["ways"][i]["return"]/investisment)
        labels2.append(f'Best way n°{i+1} : {round(json_file["ways"][i]["return"]/investisment,4)}')
    
    fig = go.Figure(
        data=go.Bar(
            x=ways,
            y=investisment_pourcentage,
            text='',#labels,
            name="Pourcentage of return",
            hovertemplate=labels2,
            marker=dict(color="paleturquoise"),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=ways,
            y=returns,
            yaxis="y2",
            mode='lines+markers', 
            text=labels,
            name="Evolution of the differents return",
            marker=dict(color="crimson"),
        )
    )

    fig.update_layout(
       title='Evolution of Return', 
        xaxis_title='Way Index',
        legend=dict(x=0.42, y=0.98),
        showlegend=True,
        yaxis=dict(
            title=dict(text="Pourcentage of return"),
            side="right",
            range=[min(investisment_pourcentage)*0.9995, max(investisment_pourcentage)],
        ),
        yaxis2=dict(
            title=dict(text="Returns"),
            side="left",
            range=[round(min(returns))-1, round(max(returns))+1],
            overlaying="y",
            tickmode="sync",
        ),
    )
    return fig

st.write(differents_returns(Json_Return_sorted,investisment))

#---- Number of visualized data

st.write(Json_Return_sorted)


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
