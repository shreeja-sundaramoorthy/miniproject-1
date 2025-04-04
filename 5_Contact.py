import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Contact Information",
    page_icon="📞",
)

connection = sqlite3.connect("food_waste_management.db")
cursor = connection.cursor()

st.title("Contact Information")

@st.cache_data
def contact_provider(primary_key):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('select name,type,address,city,contact FROM providers WHERE provider_id = ?', (primary_key,))
    result = c.fetchone()
    return result
    conn.commit()
    conn.close()

@st.cache_data
def contact_receiver(primary_key):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('select name,type,city,contact FROM receivers WHERE receiver_id = ?', (primary_key,))
    result = c.fetchone()
    return result
    conn.commit()
    conn.close()


option = st.selectbox("Select an option:",['Select any','Provider','Receiver'])
if option == 'Provider':
    primary_key = st.text_input("Enter Provider_id")
    if primary_key:
        if st.button("View"):
            filter = pd.DataFrame(contact_provider(primary_key),columns=["Provider_Information"])
            filter.index = [''] * len(filter)
            st.table(filter)
    else:
        st.warning("Please fill in provider_id to view contact information")

if option == 'Receiver':
    primary_key = st.text_input("Enter receiver_id")
    if primary_key:
        if st.button("View"):
            filter = pd.DataFrame(contact_receiver(primary_key),columns=["Receiver_Information"])
            filter.index = [''] * len(filter)
            st.table(filter)
    else:
        st.warning("Please fill in provider_id to view contact information")