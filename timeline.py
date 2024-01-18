import streamlit as st
import pandas as pd
import seaborn as sns
import os, sys, datetime, math
from io import StringIO
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go



class TimeLineViz:
    
    def __init__(self, data_frame):
        self.data_frame = data_frame
    
    def chartViz(self):
        # Create subplots with shared x-axis
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=['Scatter Plot', 'Bar Chart'])
        
            # Scatter Plot
        scatter_trace = go.Scatter(
            x=self.data_frame['Week'],
            y=self.data_frame['Data science: (Worldwide)'],
            mode='markers',
            marker=dict(size=3, color='#046ccc'),
            name='Scatter Plot',
        )
        fig.add_trace(scatter_trace, row=1, col=1)

        # Bar Chart
        bar_trace = go.Bar(
            x=self.data_frame['Week'],
            y=self.data_frame['Data science: (Worldwide)'],
            marker=dict(color='#45d4b4'),
            name='Bar Chart',
        )
        fig.add_trace(bar_trace, row=2, col=1)

        # Customize the layout
        fig.update_layout(
            height=600,
            width=800,
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