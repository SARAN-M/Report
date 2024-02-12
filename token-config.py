import pandas as pd
import requests
import streamlit as st
from streamlit_pagination import pagination_component

# Customize and comment your CSS file style.css accordingly
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

# Sample DataFrame for demonstration (replace with your actual data)
data_df = pd.DataFrame()


if 'table' not in st.session_state:
    if data_df.empty:
        st.session_state['table'] = data_df
        st.session_state['df_empty'] = "true"
    else:
        st.session_state['df_empty'] = "false"
    
    
# API data retrieval and configuration (replace with your actual API interaction)
def mask_api_configuration_data():
    try:
        response = requests.get("http://localhost:3000/data-scan/token-configuration")
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
        if key == 'tokenName':
            column_config[key] = st.column_config.TextColumn(
            value,
            help="Streamlit **widget** commands 🎈",
            max_chars=50,
            required=True,
            validate="^[a-z]+$",
        )
        elif key == 'type':
            column_config[key] = st.column_config.TextColumn(
            value,
            default="custom",
            help="Streamlit **widget** commands 🎈",
            disabled="true",
            required=True,
        )
        elif key == 'noOfBytes':
            column_config[key] = st.column_config.SelectboxColumn(
            value,
            options=["Random", "Same as input"],
            help="Streamlit **widget** commands 🎈",
            required=True,
        )
        elif key == 'minBytes':
            column_config[key] = st.column_config.NumberColumn(
            value,
            help="Streamlit **widget** commands 🎈",
            min_value=0,
            # max_value=100000,
            # step=1,
            format="%d",
            required=True,
        )
        elif key == 'maxBytes':
            column_config[key] = st.column_config.NumberColumn(
            value,
            help="Streamlit **widget** commands 🎈",
            # min_value=0,
            # max_value=1000,
            # step=1,
            format="%d",
            required=True,
        )
        elif key == 'tokenCharacters':
            column_config[key] = st.column_config.SelectboxColumn(
            value,
            options=["Numeric", "Alpha-numeric"],
            help="Streamlit **widget** commands 🎈",
            default="",
            required=True,
        )
        elif key == 'caseSensitive':
            column_config[key] = st.column_config.SelectboxColumn(
            value,
            options=["Yes","No"],
            help="Streamlit **widget** commands 🎈",
            default="",
            required=True,
        )
    return column_config 

# Pagination parameters
page_size = 4  # Number of rows per page

print("intializing")
print(st.session_state['table'])

def data_chunk_choice():
    # Replace with your preferred logic to handle session state and data chunks
    if 'foo' not in st.session_state or st.session_state['foo'] is None:
        return 0
    return st.session_state['foo']


def on_change(data):
    print('on_change')
    print(pd.DataFrame(data))
    if 'table' in st.session_state:
        st.session_state['table'][:] = pd.DataFrame(data).copy()  # Update session data using a copy

# Function to display a paginated data editor with advanced search
def display_page(page_num, isDFEmpty):
    print('display_page',isDFEmpty)
        # API data handling (replace with actual logic)
    api_data = mask_api_configuration_data()
    columns = format_data(api_data["data"]["columns"])
    if isDFEmpty:
        data_df =  pd.DataFrame(api_data["data"]["data"])
        start_index = (page_num - 1) * page_size
        end_index = start_index + page_size
        page_data = data_df.iloc[start_index:end_index]

    # Search functionality:
        query = st.text_input("Search", placeholder="Enter search term(s)")
        if query:
            search_mask = page_data.applymap(lambda x: query.lower() in str(x).lower()).any(axis=1)
            page_data = page_data[search_mask]
        st.session_state['table'] = page_data
        # Generate a unique key for the DataEditor
        unique_key = f"data_editor_{page_num}"

    # Display the DataEditor with updated data and columns:
        print("secondddddd")
        print(page_data)
        data = st.data_editor(
        st.session_state['table'].to_dict(orient="records"),
        column_config=columns,
        hide_index=True,
        key=unique_key,
        num_rows ="dynamic"
    )
    # st.session_state['table'] = data
        on_change(data)

    

    # Pagination buttons and page display:
    # Calculate total pages, display buttons, etc.

# Main execution:
display_page(1, st.session_state['df_empty'])  # Start on the first page (adjust if needed)

