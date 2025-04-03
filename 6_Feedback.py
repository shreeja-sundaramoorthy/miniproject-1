import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Feedback",
    page_icon="📝",
)

st.title("Feedback Form")

first_name = st.text_input("First name")
last_name = st.text_input("Last name")
Type = st.selectbox('choose a Type:',['Provider','Receiver','other'])
contact = st.text_input("enter your contact number")
feedback = st.text_area("Give your feedback")
if first_name and last_name and contact and feedback:
            if st.button("Submit"):
                st.success("Thanks for submitting your feedback")
else:
    st.warning("Please fill in all fields to enable the button.")