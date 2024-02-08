import pandas as pd
import requests
import streamlit as st
from streamlit_pagination import pagination_component

# Customize and comment your CSS file style.css accordingly
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

# Sample DataFrame for demonstration (replace with your actual data)
data_df = pd.DataFrame()

# API data retrieval and configuration (replace with your actual API interaction)
def mask_api_configuration_data():
    try:
        response = requests.get("http://localhost:3000/data-scan/mask-api-configuration")
    except Exception as e:
        print(e)
        raise Exception("Error in API call")
    return response.json()

# Data column configuration (replace with API logic)
def format_data(original_data):
    column_config = {}
    for item in original_data:
        key = item['key']
        value = item['value']
        if key == 'tagName':
            column_config[key] = st.column_config.TextColumn(
            value,
            help="Streamlit **widget** commands 🎈",
            default="",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        )
        elif key == 'tokenName':
            column_config[key] = st.column_config.TextColumn(
            value,
            help="Streamlit **widget** commands 🎈",
            default="",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        )
        elif key == 'prefix':
            column_config[key] = st.column_config.TextColumn(
            value,
            help="Streamlit **widget** commands 🎈",
            default="",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        )
        elif key == 'suffix':
            column_config[key] = st.column_config.TextColumn(
            value,
            help="Streamlit **widget** commands 🎈",
            default="",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        )
        elif key == 'example':
            column_config[key] = st.column_config.TextColumn(
            value,
            help="Streamlit **widget** commands 🎈",
            default="",
            max_chars=50,
            validate="^st\.[a-z_]+$",
        )
    return column_config   


# Pagination parameters
page_size = 4  # Number of rows per page

def data_chunk_choice():
    # Replace with your preferred logic to handle session state and data chunks
    if 'foo' not in st.session_state or st.session_state['foo'] is None:
        return 0
    return st.session_state['foo']

# Function to display a paginated data editor with advanced search
def display_page(page_num):
        # API data handling (replace with actual logic)
    api_data = mask_api_configuration_data()
    columns = format_data(api_data["data"]["columns"])
    data_df =  pd.DataFrame(api_data["data"]["data"])
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    page_data = data_df.iloc[start_index:end_index]

    # Search functionality:
    query = st.text_input("Search", placeholder="Enter search term(s)")
    if query:
        # Implement case-insensitive, partial-word, and keyword search as needed
        search_mask = page_data.applymap(lambda x: query.lower() in str(x).lower()).any(axis=1)
        page_data = page_data[search_mask]

    # Generate a unique key for the DataEditor
    unique_key = f"data_editor_{page_num}"

    # Display the DataEditor with updated data and columns:
    data = st.data_editor(
        page_data.to_dict(orient="records"),
        column_config=columns,
        hide_index=True,
        key=unique_key,
        num_rows ="dynamic"
    )

    # Pagination buttons and page display:
    # Calculate total pages, display buttons, etc.

# Main execution:
display_page(1)  # Start on the first page (adjust if needed)

