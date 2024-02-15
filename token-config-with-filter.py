import pandas as pd
import requests
import streamlit as st
from streamlit_pagination import pagination_component

# Customize and comment your CSS file style.css accordingly
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

# Sample DataFrame for demonstration (replace with your actual data)
data_df = pd.DataFrame()

if 'removed_columns' not in st.session_state:
    st.session_state['removed_columns'] = []

if 'table' not in st.session_state:
    if data_df.empty:
        st.session_state['table'] = data_df
        st.session_state['df_empty'] = "true"
    else:
        st.session_state['df_empty'] = "false"
    
    
# API data retrieval and configuration (replace with your actual API interaction)
def token_configuration_data():
    try:
        response = requests.get("http://localhost:3000/data-scan/token-configuration")
    except Exception as e:
        print(e)
        raise Exception("Error in API call")
    return response.json()

def update_token_configuration_data(data):
    for key, value in data.iloc[-1].to_dict().items():
        if key in ['minBytes', 'maxBytes']:
            data[key] = int(value)
    api_url = "http://localhost:3000/data-scan/token-configuration"
    updated_data = {
        "data" : [data.iloc[-1].to_dict()] }
    try:
        response = requests.put(api_url, json = updated_data)
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

def on_change(data):
    print('on_change')
    print(pd.DataFrame(data))
    if 'table' in st.session_state:
        st.session_state['table'][:] = pd.DataFrame(data).copy()  # Update session data using a copy

# Function to display a paginated data editor with advanced search
def display_page(page_num, isDFEmpty):
    # API data handling (replace with actual logic)
    api_data = token_configuration_data()
    columns = format_data(api_data["data"]["columns"])
    
    if st.session_state['table'].empty:
        data_df = pd.DataFrame(api_data["data"]["data"])
        st.session_state['table'] = data_df  # Set the table session state with the DataFrame
    else:
        data_df = st.session_state['table']
    
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
    removed_columns = st.session_state.get('removed_columns', [])  # Initialize if not in session state

    # Get the list of available columns based on the selected columns and removed columns
    available_columns = [col for col in columns if col not in removed_columns]

    # Allow user to select columns to display
    selected_columns = st.multiselect("Select columns to display:", available_columns, default=available_columns)

    if selected_columns:
        # Filter the DataFrame based on selected columns
        data_df_filtered = data_df[selected_columns]
        
        # Update session state with filtered data
        st.session_state['table'] = data_df_filtered
        
        # Display the DataEditor with updated data and columns
        data = st.data_editor(
            st.session_state['table'].to_dict(orient="records"),
            column_config=columns,
            hide_index=True,
            key=unique_key,
            num_rows="dynamic"
        )
    else:
        # Display a message if no columns are selected
        st.write("Please select at least one column to display.")

    # Update session state with the edited data
    if selected_columns:
        edited_data_df = pd.DataFrame(data)
        if len(edited_data_df) > len(page_data):
            print("sddfsrtterttrt")
            x = update_token_configuration_data(edited_data_df)
            print(x)
            added_rows = edited_data_df.iloc[len(page_data):]
            data_df = pd.concat([data_df, added_rows], ignore_index=True)
            st.session_state['table'] = data_df
        else:
            data_df.iloc[start_index:end_index] = edited_data_df
            st.session_state['table'].iloc[start_index:end_index] = pd.DataFrame(data)

# Main execution:
display_page(1, st.session_state['df_empty'])
