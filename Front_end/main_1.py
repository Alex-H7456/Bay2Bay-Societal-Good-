import streamlit as st
import pandas as pd
import numpy as np
import time 

#potential to introduce caching and advanced features later

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")
st.write("This is page 2 content.")

#st.write used automatically even wen ommited
st.write("Here's our first attempt at using data to create a table:")
chart_data = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

st.line_chart(chart_data)


map_data = pd.DataFrame(
    np.random.randn(100, 2) / [80, 80] + [51.4543, -0.9781],
    columns=['lat', 'lon'])

st.map(map_data)


x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)


if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data


df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })


with st.expander("See explanation"):
    option = st.sidebar.selectbox(
        'Which number do you like best?',
        df['first column'])

    'You selected: ', option








left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")


'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):  #unlike other thingies forloop suprisingly doesn't refresh the page
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'


with st.spinner("Processing your data..."):
    time.sleep(3)  # simulate long task
st.success("Done!")