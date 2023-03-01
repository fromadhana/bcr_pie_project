import streamlit as st
from datetime import datetime
import time


# Section 1
button = st.button('Button')
button_placeholder = st.empty()
button_placeholder.write(f'button = {button}')
time.sleep(2)
button = False
button_placeholder.write(f'button = {button}')

# Section 2
time_placeholder = st.empty()

while True:
    timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_placeholder.write(timenow)
    time.sleep(1)