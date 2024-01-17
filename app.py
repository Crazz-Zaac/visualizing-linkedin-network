import streamlit as st
import pandas as pd
import seaborn as sns
import os, sys, datetime, math
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx

from settings import DATASET_DIR, IMG_DIR
from connection import ConnectionViz


st.header("Visualizing :blue[LinkedIn] Data")

def loadDataset(dir, filename):
    data_frame = pd.read_csv(dir+filename)
    return data_frame

def bubbleChartViz(data_frame):
    
    # Create subplots with shared x-axis
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=['Scatter Plot', 'Bar Chart'])
    
        # Scatter Plot
    scatter_trace = go.Scatter(
        x=data_frame['Week'],
        y=data_frame['Data science: (Worldwide)'],
        mode='markers',
        marker=dict(size=3, color='#046ccc'),
        name='Scatter Plot',
    )
    fig.add_trace(scatter_trace, row=1, col=1)

    # Bar Chart
    bar_trace = go.Bar(
        x=data_frame['Week'],
        y=data_frame['Data science: (Worldwide)'],
        marker=dict(color='#45d4b4'),
        name='Bar Chart',
    )
    fig.add_trace(bar_trace, row=2, col=1)

    # Customize the layout
    fig.update_layout(
        height=600,
        title='Combined Scatter Plot and Bar Chart for Data Science Worldwide',
        xaxis_title='Week',
        yaxis_title='Data Science Count',
    )




    # Customize the layout if needed
    fig.update_layout(
        xaxis_title='Week',
        yaxis_title='Data Science Count',
    )

    # Display the figure
    st.plotly_chart(fig)

def main():
    st.sidebar.header("Select Options")
    # with st.sidebar.form(key='form_one'):
    option = st.sidebar.radio(
        'Make a choice',
        ('Explore Connection Data',
            'Visualize Data Science World-wide Trend',
            'Explore Company Follows Data')
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
    
    elif option == 'Visualize Data Science World-wide Trend':
        st.subheader('What is the trend of Data Science world wide?')
        df = loadDataset(DATASET_DIR, 'multiTimeline.csv')
        df['Week'] = pd.to_datetime(df['Week'])
        st.write(df.head())
        bubbleChartViz(df)


if __name__ == '__main__':
    main()