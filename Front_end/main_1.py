import streamlit as st
import pandas as pd
import numpy as np
import time 

#potential to introduce caching and advanced features later

st.sidebar.markdown("# 🧬 Add submission ")

import sys
import os

# Add parent folder to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


import streamlit as st
import time 

import pandas as pd



def receive_input(Message: str, crypt: str, height_: int = 50):
    with st.form(key=crypt):
        user_input = st.text_area(Message, height = height_, max_chars=200)
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            st.session_state[crypt] = user_input




@st.cache_resource
def load_vectors():
    return pd.read_parquet("drug_reviews_with_embeddings.parquet")

df_database = load_vectors()

st.markdown("<h1 style='text-align: center;'> 🧬 Add a Submission</h1>", unsafe_allow_html=True)
 #this is the front thing
st.sidebar.markdown("# 🧬 Med Source")

#use keys to segregate different parts of the page in a session
#all callables are temporary 

with st.sidebar:
    with st.container(border = True):
        st.markdown("<h2 style='text-align: center;'>Welcome to Med Source</h2>", unsafe_allow_html=True)
        st.write("Make an entry into the Med Source Database to help future patients.")
    st.markdown("------")
    st.markdown("<h2 style='text-align: center;'>Workflow Content</h2>", unsafe_allow_html=True)




#input now saved in session state dictirnary

receive_input("Join a community of patients: Add Review", "Review_input", 50)



st.markdown(
    """
    <div style="color: black; font-size:12px; margin:0; padding:0;">
        Your Patient ID will be generated
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("------")

            

if "Review_input" in st.session_state:
    st.write("Review submitted")
    st.write("Patient ID")
    st.write(st.session_state["Review_input"])