import streamlit as st
import time 


def receive_input():
    with st.form(key='input_form'):
        user_input = st.text_area("Enter your text here:", height = 50, max_chars=200)
        submit_button = st.form_submit_button(label='Submit')
        
        if submit_button:
            st.session_state['user_input'] = user_input
            #st.success("Input received!")


def loading_animation(interval: int =2):
    placeholder = st.empty()
    loading_text = "Loading"
    interval = int(interval / 0.2)  # Convert seconds to number of iterations
    for i in range(interval):  # 6 iterations
        dots = "." * (i % 8)  # cycles through "", ".", "..", "..."
        placeholder.text(f"{loading_text}{dots}")
        time.sleep(0.2)  # wait half a second

    placeholder.text("Done loading!")  # final message after loading

Query_time = 5

st.markdown("<h1 style='text-align: center;'>Enter Name </h1>", unsafe_allow_html=True)
 #this is the front thing
st.sidebar.markdown("# 🏠 Enter Name")

#use keys to segregate different parts of the page in a session
#all callables are temporary 

with st.sidebar:
    with st.container(border = True):
        st.markdown("<h2 style='text-align: center;'>Welcome to Enter Name</h2>", unsafe_allow_html=True)
        st.write("This is our submission for the Bay2Bay Hackathon 2025.")
    st.markdown("------")
    st.markdown("<h2 style='text-align: center;'>Workflow Content</h2>", unsafe_allow_html=True)




#input now saved in session state dictionary
receive_input()

st.markdown("------")

if 'user_input' in st.session_state:
    st.sidebar.write("Search:", st.session_state['user_input'])

    loading_animation(Query_time)
    st.sidebar.write(f"Query Time: {Query_time} seconds")
        

    with st.expander("View Input"):
        st.write("something meaningful")
