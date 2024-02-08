import pandas as pd
import streamlit as st
from streamlit_pagination import pagination_component

st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

# Dataframe
data_df = pd.DataFrame(
    {
        "tokenName": ["Default", "Test Token", "Numeric token", "AlphaNumeric token","Default1", "Test Token1", "Numeric token1", "AlphaNumeric token1", "Default", "Test Token", "Numeric token", "AlphaNumeric token","Default1", "Test Token1", "Numeric token1", "AlphaNumeric token1", ],
        "price": [20, 950, 250, 500, 30, 350, 750, 100, 20, 950, 250, 500, 30, 350, 750, 100],
        "category": [
            " Data Exploration",
            " Data Visualization",
            " LLM",
            " Data Exploration",
            " Data Exploration",
            " Data Visualization",
            " LLM",
            " Data Exploration",
            " Data Exploration",
            " Data Visualization",
            " LLM",
            " Data Exploration",
            " Data Exploration",
            " Data Visualization",
            " LLM",
            " Data Exploration",
        ],
    }
)

# Pagination parameters
page_size = 4  # Number of rows per page

def data_chunk_choice():
    if 'foo' not in st.session_state or st.session_state['foo'] is None:
        return 0
    return st.session_state['foo']

# Function to display a paginated data editor
def display_page(page_num):
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    page_data = data_df.iloc[start_index:end_index]

    # Generate a unique key for the DataEditor
    unique_key = f"data_editor_{page_num}"

    data = st.data_editor(
        page_data,
        column_config={
            "tokenName": st.column_config.TextColumn(
                "Token Name",
                help="Streamlit **widget** commands 🎈",
                default="st.",
                max_chars=50,
                validate="^st\.[a-z_]+$",
            ),
            "category": st.column_config.SelectboxColumn(
                "App Category",
                help="The category of the app",
                width="medium",
                options=[
                    "Data Exploration",
                    "Data Visualization",
                    "LLM",
                ],
                required=True,
            ),
            "price": st.column_config.NumberColumn(
                "Price (in USD)",
                help="The price of the product in USD",
                min_value=0,
                max_value=1000,
                step=1,
                format="$%d",
            )
        },
        hide_index=True,
        key=unique_key,  # Assign the unique key
    )

    n = 100
    list_df = [data[i:i+n] for i in range(0, data.shape[0], n)] 
    data_l = list_df[data_chunk_choice()] 

    # Display the pagination component below the table
    pagination_component(len(list_df), layout={"color": "primary", "style": {"margin-top": "10px"}}, key="foo")

# Calculate total pages
num_pages = (len(data_df) + page_size - 1) // page_size

# Initialize page_num
page_num = 1  # Start with the first page

# Create individual page buttons
page_buttons = []
for i in range(1, num_pages + 1):
    button = st.button(f"{i}")
    if button:
        page_num = i

# Previous and next buttons
col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column widths as needed
if col1.button("Previous"):
    page_num = max(1, page_num - 1)
if col3.button("Next"):
    page_num = min(num_pages, page_num + 1)

# Re-display the selected page
query = st.text_input("Filter")
if query:
    mask = data_df.applymap(lambda x: query in str(x).lower()).any(axis=1)
    data_df = data_df[mask]
display_page(page_num)

# Current page display
st.markdown(f"**Page {page_num} of {num_pages}**")
