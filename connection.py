import streamlit as st
import pandas as pd
import seaborn as sns
import os, sys, datetime, math
from io import StringIO
import plotly.express as px



class ConnectionViz:
    
    def __init__(self, data_frame):
        self.data_frame = data_frame
    
    
    # vewing data 
    def viewData(self):
        st.subheader("View dataset")
        items_per_page = 10
        page_number = st.number_input("Select a page number", min_value=1, value=1)
        
        # Sort the DataFrame by the 'Company' column
        self.data_frame = self.data_frame.sort_values(by=['First Name', 'Last Name'])
        self.data_frame = self.data_frame.drop('URL', axis=1)
        total_pages = math.ceil(len(self.data_frame) / items_per_page)
        page_number = max(1, min(page_number, total_pages))
        
        start_index = (page_number - 1) * items_per_page
        end_index = min(start_index + items_per_page, len(self.data_frame))
        
        styled_df = self.data_frame.iloc[start_index:end_index].style
                
        # Display dataframe with pagination
        styled_df = styled_df.set_table_styles(
            [{'selector': 'table', 
                'props': [('width', '800px'), ('height', '800px')]
                }]
        )
        st.write(styled_df)
        
        # Display "Page X of Y" indicator
        st.text(f"Page {page_number} of {total_pages}")

    def describeData(self):
        st.subheader("An overview of the data")
        buffer = StringIO()
        self.data_frame.info(buf=buffer)
        info_str = buffer.getvalue()

        # Remove unnecessary lines
        info_lines = info_str.split('\n')[5:-3]
        formatted_info = '\n'.join(info_lines)

        # Display the formatted information using st.write()
        st.text(formatted_info)
        # st.table(self.data_frame.count())

    def companyCount(self):
        # Filter out NaN values in the 'Company' column
        st.subheader("What percent of my connection belong to which company?")
        df_filtered = self.data_frame[self.data_frame['Company'].notna()]
        
        # Count values and filter by count
        df_company_counts = df_filtered['Company'].value_counts().reset_index()
        df_company_counts.columns = ['Company', 'Count']
        df_company_counts = df_company_counts.loc[df_company_counts['Count'] >= 4]
        
                
        # Displaying
        fig = px.pie(df_company_counts, names='Company', values='Count', title='Linkedin Connection grouping by Company')
        fig.update_layout(
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=True
        )
        
        st.plotly_chart(fig)

    def countYearAndMonth(self):
        st.subheader("Which year and month did I make the most connection?")
        self.data_frame['Connected On'] = pd.to_datetime(self.data_frame['Connected On'], errors='coerce')

        # Extract year and month from the 'Connected On' column
        self.data_frame['Year'] = self.data_frame['Connected On'].dt.year
        self.data_frame['Month'] = self.data_frame['Connected On'].dt.strftime('%b')  # Short month names

        # Set custom order for months
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.data_frame['Month'] = pd.Categorical(self.data_frame['Month'], categories=month_order, ordered=True)

        # Create a DataFrame with all combinations of years and months
        all_months = pd.MultiIndex.from_product([self.data_frame['Year'].unique(), self.data_frame['Month'].unique()], names=['Year', 'Month']).to_frame(index=False)
        all_months.columns = ['Year', 'Month']

        # Merge the complete DataFrame with the actual connection data
        df_full = pd.merge(all_months, self.data_frame.groupby(['Year', 'Month']).size().reset_index(name='Connection Count'), how='left', on=['Year', 'Month'])
        df_full['Connection Count'].fillna(0, inplace=True)

        # Exclude years with no connections
        df_full = df_full[df_full['Connection Count'] > 0]

        # Arrange the years and months in ascending order
        df_full = df_full.sort_values(by=['Year', 'Month'])

        # Create a bar chart to visualize connections by year
        fig_year = px.bar(
            df_full,
            x='Year',
            y='Connection Count',
            labels={'Year': 'Year', 'Connection Count': 'Connection Count'},
            title='Overview of Total Connections Per Year'
        )

        # Customize the layout if needed
        fig_year.update_layout(
            xaxis_title='Years',
            yaxis_title='Connection Count',
            xaxis=dict(tickmode='linear'),
        )

        # Display the figure for total connections per year
        st.plotly_chart(fig_year)

        # Allow the user to select a specific year for monthly connections
        selected_year = st.selectbox('Select a year to visualize monthly connections:', df_full['Year'].unique())

        # Filter data for the selected year
        df_selected_year = df_full[df_full['Year'] == selected_year]

        # Create a bar chart to visualize monthly connections for the selected year
        fig_month = px.bar(
            df_selected_year,
            x='Month',
            y='Connection Count',
            labels={'Month': 'Month', 'Connection Count': 'Connection Count'},
            title=f'Monthly Connections in {selected_year}'
        )

        # Customize the layout if needed
        fig_month.update_layout(
            xaxis_title='Month',
            yaxis_title='Connection Count',
            xaxis=dict(tickmode='linear'),
        )

        # Display the figure for monthly connections in the selected year
        st.plotly_chart(fig_month)
        

    def viewGraph(self):
        st.subheader("Who is working in what position from my connection?")
        # Create a directed graph using Plotly Express
        fig = px.scatter(
            self.data_frame,
            x='Company',
            y='Position',
            color='Position',
            hover_name='First Name',
            title='LinkedIn Connections Grouped by Positions',
        )

        # Customize the layout if needed
        fig.update_layout(
            showlegend=True,
            hovermode='closest',
            height=800,
            width=1000,
        )
        st.plotly_chart(fig)
        
