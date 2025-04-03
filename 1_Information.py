import streamlit as st
import pandas as pd
import sqlite3

connection = sqlite3.connect("food_waste_management.db")
cursor = connection.cursor()

st.set_page_config(
    page_title="Information",
    page_icon="🔍",
)

st.title("Database Information")

def read_provider():
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('SELECT * FROM providers')
    data = c.fetchall()
    conn.close()
    return data

def read_receiver():
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('SELECT * FROM receivers')
    data = c.fetchall()
    conn.close()
    return data

def read_foodlisting():
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('SELECT * FROM food_listings')
    data = c.fetchall()
    conn.close()
    return data

def read_claim():
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    c.execute('SELECT * FROM claims')
    data = c.fetchall()
    conn.close()
    return data

options = ['Select Any','Providers','Receivers','Food Listings','Claims']

choice = st.selectbox('Select to view information',options)

if choice == 'Providers':
    if st.button('View'):
        provider = read_provider()
        df = pd.DataFrame(provider, columns=['provider_id','name','type','address','city','contact'])
        st.dataframe(df)
    name_filter = st.sidebar.text_input('Filter by name:')
    type_filter = st.sidebar.multiselect('Filter by type:',['Supermarket','Grocery Store','Restaurant','Catering Service'])
    city_filter = st.sidebar.text_input('Filter by City:')
    query = "SELECT * FROM providers WHERE name LIKE ? AND city LIKE ?"
    params = (f'%{name_filter}%',f'%{city_filter}%')
    df = pd.read_sql_query(query, connection, params=params)      
    if type_filter:
        query += " AND type IN ({})".format(','.join('?' * len(type_filter)))
        params += tuple(type_filter)
        filter = pd.read_sql_query(query, connection, params=params)
        if name_filter or type_filter or city_filter:
            if st.sidebar.button("Filter"):
                st.write(filter)

elif choice == 'Receivers':
    if st.button('View'):
        receiver = read_receiver()
        df = pd.DataFrame(receiver, columns=['receiver_id','name','type','city','contact'])
        st.dataframe(df)
    name_filter = st.sidebar.text_input('Filter by name:')
    type_filter = st.sidebar.multiselect('Filter by type:',['Shelter','Individual','NGO','Charity'])
    city_filter = st.sidebar.text_input('Filter by City:')
    query = "SELECT * FROM receivers WHERE name LIKE ? AND city LIKE ? "
    params = (f'%{name_filter}%',f'%{city_filter}%')
    df = pd.read_sql_query(query, connection, params=params)      
    if type_filter:
        query += " AND type IN ({})".format(','.join('?' * len(type_filter)))
        params += tuple(type_filter)
        filter = pd.read_sql_query(query, connection, params=params)
        if name_filter or type_filter or city_filter:
            if st.sidebar.button("Filter"):
                st.write(filter)

elif choice == 'Food Listings':
    if st.button('View'):
        food_listings = read_foodlisting()
        df = pd.DataFrame(food_listings, columns=['food_id','food_name','quantity','expiry_date','provider_id','provider_type','location','food_type','meal_type'])
        st.dataframe(df)
    foodname_filter = st.sidebar.text_input('Filter by food_name:')
    providertype_filter = st.sidebar.multiselect('Filter by provider type:',['Grocery Store','Catering Service','Restaurant','Supermarket',])
    location_filter = st.sidebar.text_input('Filter by Location:')
    foodtype_filter = st.sidebar.multiselect('Filter by food type:',['Non-Vegetarian','Vegan','Vegetarian'])
    mealtype_filter = st.sidebar.multiselect('Filter by meal type:',['Breakfast','Dinner','Lunch','Snacks'])
    query = "SELECT * FROM food_listings WHERE food_name LIKE ? AND Location LIKE ? "
    params = (f'%{foodname_filter}%',f'%{location_filter}%')
    df = pd.read_sql_query(query, connection, params=params)      
    if providertype_filter:
        query += " AND provider_type IN ({})".format(','.join('?' * len(providertype_filter)))
        params += tuple(providertype_filter)
    if foodtype_filter:
        query += " AND food_type IN ({})".format(','.join('?' * len(foodtype_filter)))
        params += tuple(foodtype_filter)
    if mealtype_filter:
        query += " AND meal_type IN ({})".format(','.join('?' * len(mealtype_filter)))
        params += tuple(mealtype_filter)
    filter = pd.read_sql_query(query, connection, params=params)
    if foodname_filter or providertype_filter or location_filter or foodtype_filter or mealtype_filter:
        if st.sidebar.button("Filter"):
            st.write(filter)
elif choice == 'Claims':
    if st.button('View'):
        claims = read_claim()
        df = pd.DataFrame(claims, columns=['claim_id','food_id','receiver_id','status','time_stamp'])
        st.dataframe(df)
    status_filter = st.sidebar.multiselect('Filter by status:',['Completed','Pending','Cancelled'])
    query = "SELECT * FROM claims"
    params = ()
    df = pd.read_sql_query(query, connection, params=params)      
    if status_filter:
        query += " WHERE status IN ({})".format(','.join('?' * len(status_filter)))
        params += tuple(status_filter)
        filter = pd.read_sql_query(query, connection, params=params)
        if status_filter:
            if st.sidebar.button("Filter"):
                st.write(filter)
else:
    st.write("Please select an option to display content.")

# # Filter options
# name_filter = st.sidebar.text_input('Filter by name:')
# type_filter = st.sidebar.multiselect('Filter by type:',['Supermarket','Grocery Store','Restaurant','Catering Service'])
# city_filter = st.sidebar.text_input('Filter by City:')

# # Query with filters
# query = "SELECT * FROM users WHERE name LIKE ? AND city LIKE ? "
# params = (f'%{name_filter}%',f'%{city_filter}%')
# df = pd.read_sql_query(query, conn, params=params)

# # Display the data
# st.dataframe(df)

# # Close the connection
# conn.close()

# department_filter = st.multiselect('Filter by department:', ['HR', 'IT', 'Finance'])
# salary_filter = st.slider('Filter by salary:', 0, 100000, (0, 100000))

# Query with filters
# query = "SELECT * FROM employees WHERE salary BETWEEN ? AND ?"
# params = (salary_filter[0], salary_filter[1])

# if type_filter:
#     query += " AND type IN ({})".format(','.join('?' * len(type_filter)))
#     params += tuple(type_filter)

# filter = pd.read_sql_query(query, conn, params=params)

# Display the data
# st.dataframe(df)


# filter_column = st.sidebar.selectbox('Select a column to filter',['provider_id','name','type','address','city','contact'])
#         filter_value = st.sidebar.text_input('Enter the value to filter by')

# filter_column = st.sidebar.selectbox('Select a column to filter',df.columns)
# filter_value = st.sidebar.text_input('Enter the value to filter by')

# if filter_value:
#     filtered_df = dataframes[selected_df][dataframes[selected_df][filter_column] == filter_value]
#     st.write(f'Filtered {selected_df} by {filter_column} = {filter_value}')
#     st.dataframe(filtered_df)


# name_filter = st.sidebar.text_input('Filter by name:')
# type_filter = st.sidebar.multiselect('Filter by type:',['Supermarket','Grocery Store','Restaurant','Catering Service'])
# city_filter = st.sidebar.text_input('Filter by City:')
# query = "SELECT * FROM providers WHERE name LIKE ? AND city LIKE ? "
# params = (f'%{name_filter}%',f'%{city_filter}%')
# df = pd.read_sql_query(query, connection, params=params)      
# if type_filter:
#     query += " AND type IN ({})".format(','.join('?' * len(type_filter)))
#     params += tuple(type_filter)
#     filter = pd.read_sql_query(query, connection, params=params)
#     st.write(filter)

# if providertype_filter or foodtype_filter or mealtype_filter:
#         query += " AND provider_type IN ({}) AND food_type IN ({}) AND meal_type IN ({})".format((','.join('?' * len(providertype_filter))),(','.join('?' * len(foodtype_filter))),(','.join('?' * len(mealtype_filter))))
#         params += tuple(providertype_filter,foodtype_filter,mealtype_filter)
#         filter = pd.read_sql_query(query, connection, params=params)