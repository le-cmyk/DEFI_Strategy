import pandas as pd
import streamlit as st

from Functions.Essential_for_ProjectLine import ProjectLine, group_by_borrow


# ---- Creation and population of the projects

def creation_projects_line(df):
    project_lines = [ProjectLine(**row) for index, row in df.iterrows()]

    # Populate the projects

    project_lines_groups = group_by_borrow(project_lines)
    for project_line in project_lines:
        project_line.set_next_possible_way(project_lines_groups)
    return project_lines

# ---- Generation of all the possible ways (naive function)

def generate_all_possible_ways(starting_project_line, n, project_lines,finish_by):
    if n == 0:
        return [(starting_project_line,)]
    else:
        ways = []
        for next_project_line in starting_project_line.next_possible:
            next_ways = generate_all_possible_ways(next_project_line, n-1, project_lines,finish_by)
            for way in next_ways:
                if finish_by is None or way[-1].Lend==finish_by :
                    ways.append((starting_project_line,) + way)
        return ways
    
# ---- Creation Of a list of all possible ways 

def creation_all_possible_ways(project_lines,jump_number,start_by=None,finish_by=None):
    all_ways = []
    for project_line in project_lines:
        if start_by is None or project_line.Borrow == start_by:
            ways = generate_all_possible_ways(project_line, jump_number, project_lines,finish_by)
            all_ways.extend(ways)
    return all_ways

# ---- Creation of a list of dictionnary for all returns

def creation_all_returns(all_ways,investisment,duration_year=1):
    returns = [] # A savoir que la liste returns va contenir tout les returns pour chaque projets

    for way in all_ways:
        remaining_amount = investisment
        way_dict = {'way': [],
                    'apy': [],
                    'return': 0}
        for project_line in way:
            way_dict['return'] +=project_line.calculate_investment_return(remaining_amount,duration_year)
            remaining_amount = project_line.remaining_amount(remaining_amount)
            way_dict['way'].append(project_line.__str__())
            way_dict['apy'].append(project_line.Net_APY)

        returns.append(way_dict)

    return returns

# ---- Creation of the sorted dafataframe tanks to the list of dictionnary

@st.cache_data
def creation_sorted_df_retruns(returns):
    df_returns = pd.DataFrame(returns)
    df_returns = df_returns.sort_values('return', ascending=False).reset_index(drop=True)
    return df_returns