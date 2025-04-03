import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="Crud_operations",
    page_icon="⚙️",
)
st.title("Information Feed")

def add_provider(name,type,address,city,contact):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO providers (name, type,address,city,contact) VALUES (?,?,?,?,?)', (name,type,address,city,contact))
    conn.commit()
    conn.close()

def add_receiver(name,type,city,contact):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO receivers (name,type,city,contact) VALUES (?,?,?,?)', (name,type,city,contact))
    conn.commit()
    conn.close()

def add_foodlisting(food_name,quantity,expiry_date,provider_id,provider_type,location,food_type,meal_type):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO food_listings (food_name,quantity,expiry_date,provider_id,provider_type,location,food_type,meal_type) VALUES (?,?,?,?,?,?,?,?)', (food_name,quantity,expiry_date,provider_id,provider_type,location,food_type,meal_type))
    conn.commit()
    conn.close()

def add_claim(food_id,receiver_id,status,time_stamp):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('INSERT INTO claims (food_id,receiver_id,status,time_stamp) VALUES (?,?,?,?)', (food_id,receiver_id,status,time_stamp))
    conn.commit()
    conn.close()

def update_provider(provider_id, name=None, type=None, address=None, city=None, contact=None):
    conn = sqlite3.connect('food_waste_management.db')
    cursor = conn.cursor()
    
    if name:
        cursor.execute('UPDATE providers SET name = ? WHERE provider_id = ?', (name, provider_id))
    if type:
        cursor.execute('UPDATE providers SET type = ? WHERE provider_id = ?', (type, provider_id))
    if address:
        cursor.execute('UPDATE providers SET address = ? WHERE provider_id = ?', (address, provider_id))
    if city:
        cursor.execute('UPDATE providers SET city = ? WHERE provider_id = ?', (city, provider_id))
    if address:
        cursor.execute('UPDATE providers SET contact = ? WHERE provider_id = ?', (contact, provider_id))
    
    conn.commit()
    conn.close()

def update_receiver(receiver_id, name=None, type=None, city=None, contact=None):
    conn = sqlite3.connect('food_waste_management.db')
    cursor = conn.cursor()
    
    if name:
        cursor.execute('UPDATE receivers SET name = ? WHERE receiver_id = ?', (name, receiver_id))
    if type:
        cursor.execute('UPDATE receivers SET type = ? WHERE receiver_id = ?', (type, receiver_id))
    if city:
        cursor.execute('UPDATE receivers SET city = ? WHERE receiver_id = ?', (city, receiver_id))
    if contact:
        cursor.execute('UPDATE receivers SET contact = ? WHERE receiver_id = ?', (contact, receiver_id))
    
    conn.commit()
    conn.close()

def update_foodlisting(food_id, food_name=None, quantity=None,expiry_date=None,provider_id=None,provider_type=None,location=None,food_type=None,meal_type=None):
    conn = sqlite3.connect('food_waste_management.db')
    cursor = conn.cursor()
    
    if food_name:
        cursor.execute('UPDATE food_listings SET food_name = ? WHERE food_id = ?', (food_name, food_id))
    if quantity:
        cursor.execute('UPDATE food_listings SET quantity = ? WHERE food_id = ?', (quantity, food_id))
    if expiry_date:
        cursor.execute('UPDATE food_listings SET expiry_date = ? WHERE food_id = ?', (expiry_date, food_id))
    if provider_id:
        cursor.execute('UPDATE food_listings SET provider_id = ? WHERE food_id = ?', (provider_id, food_id))
    if provider_type:
        cursor.execute('UPDATE food_listings SET provider_type = ? WHERE food_id = ?', (provider_type, food_id))
    if location:
        cursor.execute('UPDATE food_listings SET location = ? WHERE food_id = ?', (location, food_id))
    if food_type:
        cursor.execute('UPDATE food_listings SET food_type = ? WHERE food_id = ?', (food_type, food_id))
    if meal_type:
        cursor.execute('UPDATE food_listings SET meal_type = ? WHERE food_id = ?', (meal_type, food_id))
    
    conn.commit()
    conn.close()

def update_claim(claim_id,food_id=None,receiver_id=None,status=None,time_stamp=None):
    conn = sqlite3.connect('food_waste_management.db')
    cursor = conn.cursor()
    
    if food_id:
        cursor.execute('UPDATE claims SET food_id = ? WHERE claim_id = ?', (food_id, claim_id))
    if receiver_id:
        cursor.execute('UPDATE claims SET receiver_id = ? WHERE claim_id = ?', (receiver_id, claim_id))
    if status:
        cursor.execute('UPDATE claims SET status = ? WHERE claim_id = ?', (status, claim_id))
    if time_stamp:
        cursor.execute('UPDATE claims SET time_stamp = ? WHERE claim_id = ?', (time_stamp, claim_id))
    
    conn.commit()
    conn.close()

def delete_provider(provider_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('DELETE FROM providers WHERE provider_id = ?', (provider_id,))
    conn.commit()
    conn.close()

def delete_receiver(receiver_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('DELETE FROM receivers WHERE receiver_id = ?', (receiver_id,))
    conn.commit()
    conn.close()

def delete_foodlisting(food_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('DELETE FROM food_listings WHERE food_id = ?', (food_id,))
    conn.commit()
    conn.close()

def delete_claim(claim_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('DELETE FROM claims WHERE claim_id = ?', (claim_id,))
    conn.commit()
    conn.close()

action = st.selectbox("Choose an action",['Select any Action','Add','Update','Delete'])

if action == 'Add':
    option = st.selectbox('Choose a Table:', ['Provider', 'Receiver','Food_listings','Claims'])
    if option == 'Provider':
        name = st.text_input("Enter your name")
        type = st.selectbox('Choose a Type:',['Supermarket','Grocery Store','Restaurant','Catering Service'])
        address = st.text_area("Provide your address")
        city = st.text_input("Enter city name")
        contact = st.text_input("Enter your contact")
        if name and address and city and contact:
            if st.button("Submit"):
                add_provider(name,type,address,city,contact)
                st.success(f"Hello {name}, Registration Successful")
        else:
            st.warning("Please fill in all fields to enable the button.")
       
    elif option == 'Receiver':
        name = st.text_input("Enter your name")
        type = st.selectbox('Choose a Type:',['Shelter','Individual','NGO','Charity'])
        city = st.text_input("Enter city name")
        contact = st.text_input("Enter your contact")
        if name and city and contact:
            if st.button("Submit"):
                add_receiver(name,type,city,contact)
                st.success(f"Hello {name}, Registration Successful")
        else:
            st.warning("Please fill in all fields to enable the button.")

    elif option == 'Food_listings':
        food_name = st.text_input("Enter food name")
        quantity = st.slider("Select quantity",1,100)
        expiry_date = st.date_input("Select expiry date")
        provider_id = st.text_input("Enter provider id")
        provider_type = st.selectbox('Choose a Type:',['Supermarket','Grocery Store','Restaurant','Catering Service'])
        location = st.text_input("Enter location")
        food_type = st.selectbox('Choose a food type:',['Non-Vegetarian','Vegan','Vegetarian'])
        meal_type = st.selectbox('Choose a meal type:',['Breakfast','Dinner','Lunch','Snacks'])
        if provider_id and location and food_name:
                if st.button("Add Food"):
                    add_foodlisting(food_name,quantity,expiry_date,provider_id,provider_type,location,food_type,meal_type)
                    st.success("Food listed sucessfully")
        else:
            st.warning("Please fill in all fields to enable the button.")

    elif option == 'Claims':
        food_id = st.text_input("Enter food id")
        receiver_id = st.text_input("Enter receiver id")
        status = st.selectbox('Choose a status:',['Completed','Pending','Cancelled'])
        date = st.date_input('Choose a date:',datetime.now().date())
        time = st.time_input("Select a time", datetime.now().time())
        time_stamp = datetime.combine(date,time)
        if food_id and receiver_id :
                if st.button("claim"):
                    add_claim(food_id,receiver_id,status,time_stamp)
                    st.success("Claim information added sucessfully")
        else:
            st.warning("Please fill in all fields to enable the button.")
    
if action == 'Update':
    option = st.selectbox('Choose a Table:', ['Provider', 'Receiver','Food_listings','Claims'])
    if option == 'Provider':
        provider_id = st.number_input("Enter Provider_id",min_value=1,max_value=2000,step=1)
        name = st.text_input("Enter name")
        type = st.selectbox('Choose a Type:',['Supermarket','Grocery Store','Restaurant','Catering Service'])
        address = st.text_area("Provide your address")
        city = st.text_input("Enter city")
        contact = st.text_input("Enter Contact information")
        if st.button("Update"):
            update_provider(provider_id, name if name else None, type if type else None, address if address else None, city if city else None, contact if contact else None)
            st.success("Provider information updated sucessfully")
        else:
            st.warning("Please fill in fields that need to be updated")

    if option == 'Receiver':
        receiver_id = st.number_input("Enter receiver_id",min_value=1,max_value=2000,step=1)
        name = st.text_input("Enter name")
        type = st.selectbox('Choose a Type:',['Shelter','Individual','NGO','Charity'])
        city = st.text_input("Enter city")
        contact = st.text_input("Enter Contact information")
        if st.button("Update"):
            update_receiver(receiver_id, name if name else None, type if type else None, city if city else None, contact if contact else None)
            st.success("Receiver information updated sucessfully")
        else:
            st.warning("Please fill in fields that need to be updated")

    if option == 'Food_listings':
        food_id = st.number_input("Enter food_id",min_value=1,max_value=2000,step=1)
        food_name = st.text_input("Enter food name")
        quantity = st.slider("Select quantity",1,100)
        expiry_date = st.date_input("Select expiry date")
        provider_id = st.text_input("Enter provider id")
        provider_type = st.selectbox('Choose a Type:',['Supermarket','Grocery Store','Restaurant','Catering Service'])
        location = st.text_input("Enter location")
        food_type = st.selectbox('Choose a food type:',['Non-Vegetarian','Vegan','Vegetarian'])
        meal_type = st.selectbox('Choose a meal type:',['Breakfast','Dinner','Lunch','Snacks'])
        if st.button("Update"):
            update_foodlisting(food_id, food_name if food_name else None, quantity if quantity else None, expiry_date if expiry_date else None, provider_id if provider_id else None, provider_type if provider_type else None,location if location else None, food_type if food_type else None, meal_type if meal_type else None)
            st.success("Food listing information updated sucessfully")
        else:
            st.warning("Please fill in fields that need to be updated")

    if option == 'Claims':
        claim_id = st.number_input("Enter claim_id",min_value=1,max_value=2000,step=1)
        food_id = st.text_input("Enter food id")
        receiver_id = st.text_input("Enter receiver id")
        status = st.selectbox('Choose a status:',['Completed','Pending','Cancelled'])
        date = st.date_input('Choose a date:',datetime.now().date())
        time = st.time_input("Select a time", datetime.now().time())
        time_stamp = datetime.combine(date,time)
        if st.button("Update"):
            update_claim(claim_id, food_id if food_id else None, receiver_id if receiver_id else None, status if status else None, time_stamp if time_stamp else None)
            st.success("Clain information updated sucessfully")
        else:
            st.warning("Please fill in fields that need to be updated")

if action == 'Delete':
    option = st.selectbox('Choose a Table:', ['Provider', 'Receiver','Food_listings','Claims'])
    if option == 'Provider':
        provider_id = st.number_input("Enter Provider_id",min_value=1,max_value=2000,step=1)
        if st.button("Delete"):
            delete_provider(provider_id)
            st.success("Provider information deleted sucessfully")
        else:
            st.warning("Please fill in provider_id to delete the information")
    
    if option == 'Receiver':
        receiver_id = st.number_input("Enter receiver_id",min_value=1,max_value=2000,step=1)
        if st.button("Delete"):
            delete_receiver(receiver_id)
            st.success("Receiver information deleted sucessfully")
        else:
            st.warning("Please fill in receiver_id to delete the information")

    if option == 'Food_listings':
        food_id = st.number_input("Enter food_id",min_value=1,max_value=2000,step=1)
        if st.button("Delete"):
            delete_foodlisting(food_id)
            st.success("Food Listing information deleted sucessfully")
        else:
            st.warning("Please fill in Food_id to delete the information")

    if option == 'Claims':
        claim_id = st.number_input("Enter claim_id",min_value=1,max_value=2000,step=1)
        if st.button("Delete"):
            delete_claim(claim_id)
            st.success("Claim information deleted sucessfully")
        else:
            st.warning("Please fill in claim_id to delete the information")

else:
    st.write("Please Choose an Action")

        







