import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Learner Queries",
    page_icon="📈",
)


st.title("Learner Analysis")

providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")
food_listings = pd.read_csv("food_listings_data.csv")
claims = pd.read_csv("claims_data.csv")

connection = sqlite3.connect("food_waste_management.db")
cursor = connection.cursor()

#query  16.which provider type have provided the least food?
query_16 = ('''
                select providers.type, sum(food_listings.quantity)
                from providers
                inner join food_listings on food_listings.provider_id = providers.provider_id
                group by providers.type
                order by sum(food_listings.quantity) asc
                limit 1 ;   
 ''')

cursor.execute(query_16)
result_16 = cursor.fetchall()

df_16 = pd.DataFrame(result_16,columns=["provider_type","quantity"])

#query  17.which city have more providers ?
query_17 = ('''
                select city,count(provider_id)
                from providers
                group by city
                order by count(provider_id) desc
                limit 1;               
 ''')

cursor.execute(query_17)
result_17 = cursor.fetchall()

df_17 = pd.DataFrame(result_17,columns=["city","no_of_providers"])

#query  18.which type of receivers claimed more food
query_18 = ('''
                select receivers.type ,sum(quantity)
                from receivers
                inner join claims on claims.receiver_id = receivers.receiver_id
                inner join food_listings on food_listings.food_id = claims.food_id
                group by receivers.type
                order by sum(quantity) desc
                limit 1;     
 ''')

cursor.execute(query_18)
result_18 = cursor.fetchall()

df_18 = pd.DataFrame(result_18,columns=["receiver_type","food_claimed"])

#query  19.top 5 city has low number of food listings
query_19 = ('''
                select location, sum(quantity) as quantity_listed
                from food_listings
                group by location
                order by quantity_listed asc
                limit 4;                  
 ''')

cursor.execute(query_19)
result_19 = cursor.fetchall()

df_19 = pd.DataFrame(result_19,columns=["city_name","food_listed"])

#query  20.top 10 provider has provided vegan foodtype
query_20 = ('''
                select providers.name as provider_name
                from providers
                join food_listings on food_listings.provider_id = providers.provider_id
                where food_listings.food_type = 'Vegan'
                order by food_listings.quantity desc
                limit 10;               
 ''')

cursor.execute(query_20)
result_20 = cursor.fetchall()

df_20 = pd.DataFrame(result_20,columns=["provider_name"])

#query  21.what is the average quantity of food donated by each provider
query_21 = ('''
                select providers.name as provider_name,avg(food_listings.quantity) as average_quantity_of_food
                from providers
                inner join food_listings on providers.provider_id = food_listings.provider_id
                group by providers.provider_id               
 ''')

cursor.execute(query_21)
result_21 = cursor.fetchall()

df_21 = pd.DataFrame(result_21,columns=["provider_name","average_quantity_of_food"])

#query  22.list top 5 provider
query_22 = ('''
                select providers.Name as provider_name, sum(food_listings.quantity) as food_contributed
                from providers
                inner join food_listings on providers.provider_id = food_listings.provider_id
                group by food_listings.provider_id
                order by food_contributed desc
                limit 5;
                
 ''')

cursor.execute(query_22)
result_22 = cursor.fetchall()

df_22 = pd.DataFrame(result_22,columns=["provider_name","Food_contributed"])


dataframes_2 = {
    'Type of provider provided least quantity of food':df_16,
    'City with more providers':df_17,
    'Type of receivers claiming more food':df_18,
    'Top 5 City with low number of food listings':df_19,
    'Top 10 provider who provides vegan food type':df_20,
    'Average quantity of food donated by each provider':df_21,
    'Top 5 provider of food with food contributed':df_22
    
}

selected_dfs_2 = st.selectbox("Select Table",list(dataframes_2.keys()))

st.write(dataframes_2[selected_dfs_2])