import sys
import os

# Add parent folder to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


import streamlit as st
import time 
import The_backend

sensitivity =0.28


def receive_input():
    with st.form(key='input_form'):
        user_input = st.text_area("Ask a community of patients:", height = 50, max_chars=200)
        submit_button = st.form_submit_button(label='Search')
        
        if submit_button:
            st.session_state['user_input'] = user_input
            #st.success("Input received!")



def backend(input: str):
    time.sleep(1)

   




st.markdown("<h1 style='text-align: center;'>Med Source</h1>", unsafe_allow_html=True)
 #this is the front thing
st.sidebar.markdown("# 🏠 Med Source")

#use keys to segregate different parts of the page in a session
#all callables are temporary 

with st.sidebar:
    with st.container(border = True):
        st.markdown("<h2 style='text-align: center;'>Welcome to Med Source</h2>", unsafe_allow_html=True)
        st.write("This is our submission for the Bay2Bay Hackathon 2025. An attempts to democratise patient information with input from AI agents powered by the open FDA database")
    st.markdown("------")
    st.markdown("<h2 style='text-align: center;'>Workflow Content</h2>", unsafe_allow_html=True)




#input now saved in session state dictionary
receive_input()
#parameters for number of entries and resolution
st.markdown(
    """
    <div style="color: black; font-size:12px; margin:0; padding:0;">
        Always consult a proffesional. This is not medical advice
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("------")

l_col, r_col = st.columns([2.5, 1.5]) 

with l_col:
    results = st.slider(
        "Select the number of reviews",
        min_value=0,
        max_value=20,
        value = 5
    )

with r_col:
    Ai_type = st.selectbox(
        "FDA AI Detail",
        options= ["Concise Search", "Deep Search"],
        index = 0
    )


st.markdown("------")

if 'user_input' in st.session_state:
    st.sidebar.write("Search:", st.session_state['user_input'])



    
    with st.spinner("Processing..."):  # Streamlit built-in spinner
        start_time = time.time()
        engine = The_backend.SearchGo(st.session_state['user_input'],results, sensitivity)
        end_time = time.time()

    st.sidebar.write(f"Query Time: {end_time-start_time:.2f} seconds")
        

    main_col, right_col = st.columns([2.5, 1.5]) 

    with main_col:
         
        st.markdown("""
        <div style='font-size:25px; margin:0; padding:0; line-height:1.2;'>Patient Reviews</div>
    """, unsafe_allow_html=True)

        if engine.output["reviews"]["score"][0] <sensitivity:
            st.write("No relevant reviews")

            
        else:
            for i in range(len(engine.output["reviews"]["DrugName"])):
                if engine.output["reviews"]["score"][i] <sensitivity:
                    st.write("No more relevant search results")
                    break
                else:
                    with st.container(border = True):
                        st.write(f"Patient ID: {engine.output['reviews']['ID'][i]}")
                        st.write(f"Drug: {engine.output['reviews']['DrugName'][i]} for {engine.output['reviews']['condition'][i]}")
                        st.write(f"{engine.output['reviews']['review'][i]}")
            


    with right_col:
        st.markdown("""
        <div style='font-size:25px; margin:0; padding:0; line-height:1.2;'>FDA Guidance</div>
    """, unsafe_allow_html=True)
        st.write("AI-powered")

        with st.container(border = True):
            if Ai_type == "Concise Search":
                st.write(f"{engine.output["AI"]["truncated"]}")
            else:
                st.write(f"{engine.output["AI"]["long"]}")



