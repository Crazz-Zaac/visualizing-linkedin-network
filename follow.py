import streamlit as st
import pandas as pd
import seaborn as sns
import os, sys, datetime, math
from io import StringIO
import plotly.express as px
import networkx as nx

class CompanyFollowViz:
    
    def __init__(self, data_frame):
        self.data_frame = data_frame
        
    def compFollow(self):
        self.data_frame['Followed On'] = pd.to_datetime(self.data_frame['Followed On'])
        
        # Create a bar chart
        fig=px.histogram(self.data_frame, x='Followed On')
        fig.update_layout(title='Follow-ups Count by Year', xaxis_title='Year', yaxis_title='Follow-ups Count')

        # Display the chart
        st.plotly_chart(fig)