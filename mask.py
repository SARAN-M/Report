import pandas as pd
import streamlit as st
from streamlit_pagination import pagination_component

st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

# Dataframe
data_df = pd.DataFrame(
    {
        "tokenName": ["Default", "Test Token", "Numeric token", "AlphaNumeric token"],
        "price": [20, 950, 250, 500],
        "category": [
            " Data Exploration",
            " Data Visualization",
            " LLM",
            " Data Exploration",
        ],
    }
)

# Pagination parameters
page_size = 2  # Number of rows per page

# Function to display a paginated data editor
def display_page(page_num):
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    page_data = data_df.iloc[start_index:end_index]

    # Generate a unique key for the DataEditor
    unique_key = f"data_editor_{page_num}"

    st.data_editor(
        page_data,
        column_config={
            # ... your column configuration ...
        },
        hide_index=True,
        key=unique_key,  # Assign the unique key
    )

# Calculate total pages
num_pages = (len(data_df) + page_size - 1) // page_size

# Initialize page_num
page_num = 1  # Start with the first page

# Display the selected page
# display_page(page_num)

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
display_page(page_num)

# Current page display
st.markdown(f"**Page {page_num} of {num_pages}**")
