import streamlit as st


# Define pages
#main_page = st.Page("app_entry.py", title="Main Page", icon="🎈")
page_2 = st.Page("main_1.py", title="Add a Review", icon="🧬")
page_3 = st.Page("main_2.py", title="Query Med Source", icon="🏠")

# Navigation
pg = st.navigation([ page_2, page_3])

# Run the selected page
pg.run()

