import streamlit as st
import pandas as pd
import seaborn as sns
import os, sys, datetime, math
from io import StringIO
import plotly.express as px
from settings import DATASET_DIR, IMG_DIR


st.header("Visualizing :blue[Linkedin] Data")

def loadDataset(dir, filename):
    data_frame = pd.read_csv(dir+filename)
    return data_frame

def viewData(data_frame):
    items_per_page = 10
    page_number = st.number_input("Select a page number", min_value=1, value=1)
    
    # Sort the DataFrame by the 'Company' column
    data_frame = data_frame.sort_values(by=['First Name', 'Last Name'])
    data_frame = data_frame.drop('URL', axis=1)
    total_pages = math.ceil(len(data_frame) / items_per_page)
    page_number = max(1, min(page_number, total_pages))
    
    start_index = (page_number - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(filtered_df))
    
    styled_df = data_frame.iloc[start_index:end_index].style
    # Highlight max values in 'total_volume' column
    # styled_df = styled_df.highlight_max(axis=0, subset=['First Name', 'Last Name', 'URL' ,'Company', 'Position', 'Connected On'])

    
    # Display dataframe with pagination
    styled_df = styled_df.set_table_styles(
        [{'selector': 'table', 
            'props': [('width', '800px'), ('height', '800px')]
            }]
    )
    st.write(styled_df)
    
    # Display "Page X of Y" indicator
    st.text(f"Page {page_number} of {total_pages}")

def describeData(data_frame):
    buffer = StringIO()
    data_frame.info(buf=buffer)
    info_str = buffer.getvalue()

    # Remove unnecessary lines
    info_lines = info_str.split('\n')[5:-3]
    formatted_info = '\n'.join(info_lines)

    # Display the formatted information using st.write()
    st.text(formatted_info)
    # st.table(data_frame.count())

def companyCount(data_frame):
    # Filter out NaN values in the 'Company' column
    df_filtered = data_frame[data_frame['Company'].notna()]
    
    # Count values and filter by count
    df_company_counts = df_filtered['Company'].value_counts().reset_index()
    df_company_counts.columns = ['Company', 'Count']
    df_company_counts = df_company_counts.loc[df_company_counts['Count'] >= 4]
    
    # Check for NaN values in the 'Company' column
    # nan_count = df_company_counts['Company'].isnull().sum()
    # print(f"Number of NaN values in 'Company' column: {nan_count}")
    
    # Displaying
    fig = px.pie(df_company_counts, names='Company', values='Count', title='Linkedin Connection grouping by Company')
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=True
    )
    
    st.plotly_chart(fig)

def countYearAndMonth(data_frame):
    data_frame['Connected On'] = pd.to_datetime(data_frame['Connected On'], errors='coerce')

    # Extract year and month from the 'Connected On' column
    data_frame['Year'] = data_frame['Connected On'].dt.year
    data_frame['Month'] = data_frame['Connected On'].dt.strftime('%b')  # Short month names

    # Set custom order for months
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data_frame['Month'] = pd.Categorical(data_frame['Month'], categories=month_order, ordered=True)

    # Create a DataFrame with all combinations of years and months
    all_months = pd.MultiIndex.from_product([data_frame['Year'].unique(), data_frame['Month'].unique()], names=['Year', 'Month']).to_frame(index=False)
    all_months.columns = ['Year', 'Month']

    # Merge the complete DataFrame with the actual connection data
    df_full = pd.merge(all_months, data_frame.groupby(['Year', 'Month']).size().reset_index(name='Connection Count'), how='left', on=['Year', 'Month'])
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

st.sidebar.header("Select Options")
# with st.sidebar.form(key='form_one'):
option = st.sidebar.radio(
    'Make a choice',
    ('Explore Connection Data',
        'Explore Timeline Data',
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
         
    view_data = st.sidebar.checkbox('View Data')
    describe_data = st.sidebar.checkbox('Describe data')
    count_company = st.sidebar.checkbox("Count data by companies")
    count_year = st.sidebar.checkbox("Connections by year and month")
    
    
    if view_data:
        viewData(filtered_df)

    
    if describe_data:
        describeData(filtered_df)
        
    if count_company:
        companyCount(filtered_df)

    if count_year:
        countYearAndMonth(filtered_df)
    
    
    
    # submit_button = st.form_submit_button(label='Submit ')