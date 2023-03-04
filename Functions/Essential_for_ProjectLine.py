import streamlit as st
import pandas as pd

#---- Creation of the ProjectLine class 

class ProjectLine:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.next_possible=[]

    def __str__(self):
        return f"Project {self.Project} Borrow:{self.Borrow} Lend: {self.Lend} LTV: {self.LTV} Net APY: {self.Net_APY}"
        
    def set_next_possible_way(self, project_lines_groups):
        self.next_possible = project_lines_groups.get(self.Lend, [])    

    def display_next_ways(self):
        print("Borrow group for", self.lend, ":")
        for i, project_line in enumerate(self.next_possible):
            print(i, project_line)

    def calculate_investment_return(self, amount):
        return amount+(amount * self.Net_APY/100)
    
    def remaining_amount(self,amount):
        return amount * self.LTV/100
    
#---- Read a csv

@st.cache_data
def get_data_from_csv(path):
    df = pd.read_csv(path).drop_duplicates()

    # Replace spaces with underscores
    df.columns = df.columns.str.replace(' ', '_')

    return df

#---- Group the projects

def group_by_borrow(project_lines):
        groups = {}
        for project_line in project_lines:
            if project_line.Borrow in groups:
                groups[project_line.Borrow].append(project_line)
            else:
                groups[project_line.Borrow] = [project_line]
        return groups

