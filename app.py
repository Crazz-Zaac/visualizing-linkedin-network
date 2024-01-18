import streamlit as st
import pandas as pd
import seaborn as sns
import os, sys, datetime, math
from io import StringIO
import plotly.express as px
import networkx as nx

from settings import DATASET_DIR, IMG_DIR
from connection import ConnectionViz
from timeline import TimeLineViz
from follow import CompanyFollowViz


st.header("Visualizing :blue[LinkedIn] Data")

def loadDataset(dir, filename):
    data_frame = pd.read_csv(dir+filename)
    return data_frame



def main():
    st.sidebar.header("Select Options")
    # with st.sidebar.form(key='form_one'):
    option = st.sidebar.radio(
        'Make a choice',
        ('Explore Connection Data',
            'Visualize Data Science World-wide Trend',
            'Explore Company Following Data')
    )
    if option == 'Explore Connection Data':
        df = loadDataset(DATASET_DIR, 'Connections.csv')  
        df.drop('Email Address', axis=1, inplace=True)  # Note: Corrected here
        df['First Name'] = df['First Name'].astype(str)
        df['Last Name'] = df['Last Name'].astype(str)
        df['URL'] = df['URL'].astype(str)
        df['Company'] = df['Company'].astype(str)
        df['Position'] = df['Position'].astype(str)
        df['Connected On'] = pd.to_datetime(df['Connected On'], errors='coerce')
        filtered_df = df[df['Company'].notna()].sort_values(by='Company')
        
        # divider line
        st.sidebar.divider()
        
        cxn = ConnectionViz(filtered_df)
                    
        view_data = st.sidebar.checkbox('View Data')
        describe_data = st.sidebar.checkbox('Describe data')
        count_company = st.sidebar.checkbox("Count data by companies")
        count_year = st.sidebar.checkbox("Connections by year and month")
        view_graph = st.sidebar.checkbox("View connection graph")
        tree_map = st.sidebar.checkbox("View Tree Map")
        # view_connexon = st.sidebar.checkbox("Maximum people involved position")
        
        
        if view_data:
            cxn.viewData()
        
        if describe_data:
            cxn.describeData()
            
        if count_company:
            cxn.companyCount()

        if count_year:
            cxn.countYearAndMonth()
        
        if view_graph:
            cxn.viewGraph()
        
        if tree_map:
            cxn.viewTreeMap()
    
    if option == 'Visualize Data Science World-wide Trend':
        st.subheader('Data Science Trend')
        df = loadDataset(DATASET_DIR, 'multiTimeline.csv')
        df['Week'] = pd.to_datetime(df['Week'])
        tml = TimeLineViz(df)
        st.write(df)
        st.subheader('What is the trend of Data Science world wide?')
        tml.chartViz()
    
    if option == 'Explore Company Following Data':
        st.subheader("How many companies did I connect with yearly?")
        d_frame = loadDataset(DATASET_DIR, 'Company Follows.csv')
        flw = CompanyFollowViz(d_frame)
        flw.compFollow()
    


if __name__ == '__main__':
    main()