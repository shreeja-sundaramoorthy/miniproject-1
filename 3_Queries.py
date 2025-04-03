import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Queries",
    page_icon="📊",
)

st.title("Analysis")

providers = pd.read_csv("providers_data.csv")
receivers = pd.read_csv("receivers_data.csv")
food_listings = pd.read_csv("food_listings_data.csv")
claims = pd.read_csv("claims_data.csv")

connection = sqlite3.connect("food_waste_management.db")
cursor = connection.cursor()

#query 1.How many food providers and receivers are there in each city?
query_1_1 = ('''
            select city, count(provider_id) from providers group by city;
 ''')
query_1_2 = ('''
            select city, count(receiver_id) from receivers group by city;
 ''')

cursor.execute(query_1_1)
result_1_1 = cursor.fetchall()

cursor.execute(query_1_2)
result_1_2 = cursor.fetchall()

df_1_1 = pd.DataFrame(result_1_1,columns=["City","no_of_food_providers"])
df_1_2 = pd.DataFrame(result_1_2,columns=["city","no_of_food_receivers"])

combined_df = pd.concat([df_1_1, df_1_2], axis=1, ignore_index=False)

#query 2.Which type of food provider (restaurant, grocery store, etc.) contributes the most food?
query_2 = ('''
            select provider_type,sum(quantity) as contributed_food
            from food_listings
            group by provider_type
            order by sum(quantity) desc
            limit 1;
 ''')

cursor.execute(query_2)
result_2 = cursor.fetchall()

df_2 = pd.DataFrame(result_2,columns=["provider_type","contributed_food"])

#query 3.What is the contact information of food providers in a specific city?
query_3 = ('''
            SELECT name,contact FROM providers
            group by city;
 ''')

cursor.execute(query_3)
result_3 = cursor.fetchall()

df_3 = pd.DataFrame(result_3,columns=["provider_name","contact"])

#query 4.Which receivers have claimed the most food?
query_4 = ('''
            select receivers.name, sum(food_listings.quantity) as food_claimed
            from receivers
            inner join claims on receivers.receiver_id = claims.receiver_id
            inner join food_listings on food_listings.food_id = claims.food_id
            group by receivers.receiver_id
            order by food_claimed desc
            limit 10;
 ''')

cursor.execute(query_4)
result_4 = cursor.fetchall()

df_4 = pd.DataFrame(result_4,columns=["receiver_name","food_claimed"])

#query 5.What is the total quantity of food available from all providers?
query_5 = ('''
            select sum(quantity) as total_quantity_of_food_available
            from food_listings
            inner join claims on claims.Food_id = food_listings.Food_id
            where claims.status != 'completed';
 ''')

cursor.execute(query_5)
result_5 = cursor.fetchall()

df_5 = pd.DataFrame(result_5,columns=["total_quantity_of_food_available"])

#query 6.Which city has the highest number of food listings?
query_6 = ('''
            select location,sum(quantity) as food_listed 
            from food_listings
            group by location
            order by food_listed desc
            limit 1;
 ''')

cursor.execute(query_6)
result_6 = cursor.fetchall()

df_6 = pd.DataFrame(result_6,columns=["location","food_listed"])

#query 7.What are the most commonly available food types?
query_7 = ('''
            select distinct(Food_type) as food_types
            from food_listings
 ''')

cursor.execute(query_7)
result_7 = cursor.fetchall()

df_7 = pd.DataFrame(result_7,columns=["food_types"])


#query  9.How many food claims have been made for each food item?
query_9 = ('''
            select food_name,count(claims.food_id) as no_of_claims
            from food_listings
            inner join claims on claims.food_id = food_listings.food_id
            group by food_name;
 ''')

cursor.execute(query_9)
result_9 = cursor.fetchall()

df_9 = pd.DataFrame(result_9,columns=["food_name","no_of_claims"])

#query  10.Which provider has had the highest number of successful food claims?
query_10 = ('''
            select providers.name, count(claims.status) as sucessful_food_claims
            from providers
            inner join food_listings on providers.provider_id = food_listings.provider_id
            inner join claims on claims.food_id = food_listings.food_id
            where claims.status = 'Completed'
            group by providers.provider_id
            order by sucessful_food_claims desc
            limit 1;
 ''')

cursor.execute(query_10)
result_10 = cursor.fetchall()

df_10 = pd.DataFrame(result_10,columns=["provider_name","Sucessful_food_claims"])

#query  12.What percentage of food claims are completed vs. pending vs. canceled?
query_12 = ('''
            select (select (count(status)*100)/(select count(*) from claims)
            from claims 
            where status = "Completed"),(select (count(status)*100)/(select count(*) from claims)
            from claims 
            where status = "Pending"),(select (count(status)*100)/(select count(*) from claims)
            from claims 
            where status = "Cancelled") from claims
            limit 1;
 ''')

cursor.execute(query_12)
result_12 = cursor.fetchall()

df_12 = pd.DataFrame(result_12,columns=["completed","pending","cancelled"])

#query  13.What is the average quantity of food claimed per receiver?
query_13 = ('''
                select receivers.name,avg(food_listings.quantity) as average_quantity_of_food_claimed_per_receiver
                from food_listings
                inner join claims on food_listings.food_id = claims.food_id
                inner join receivers on claims.receiver_id = receivers.receiver_id
                group by receivers.receiver_id;
 ''')

cursor.execute(query_13)
result_13 = cursor.fetchall()

df_13 = pd.DataFrame(result_13,columns=["receiver_name","average_quantity_of_food_claimed_per_receiver"])

#query  14.Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?
query_14 = ('''
                select food_listings.meal_type as meal_type,count(claims.claim_id)
                from food_listings
                inner join claims on claims.food_id = food_listings.food_id 
                where claims.status = 'Completed'
                group by food_listings.meal_type
                order by count(claims.claim_id)
                limit 1;
 ''')

cursor.execute(query_14)
result_14 = cursor.fetchall()

df_14 = pd.DataFrame(result_14,columns=["meal_type","no_of_claims"])

#query  15.What is the total quantity of food donated by each provider?
query_15 = ('''
                select providers.name,sum(food_listings.quantity)
                from providers
                inner join food_listings on food_listings.provider_id = providers.provider_id
                group by providers.name; 
 ''')

cursor.execute(query_15)
result_15 = cursor.fetchall()

df_15 = pd.DataFrame(result_15,columns=["provider_name","quantity_donated"])

dataframes_1 = {
    'Number of Providers and Receivers in each city': combined_df,
    'Type of Provider contributing Most food': df_2,
    'Contact information of Food Providers in each city':df_3,
    'Top 10 receivers who claimed most food':df_4,
    'Quantity of food available':df_5,
    'City with highest number of food listings':df_6,
    'Most commonly available food types':df_7,
    'Number of food claims made for each food item':df_9,
    'Provider with highest number of sucessful food claims':df_10,
    'Percentage of food claim status':df_12,
    'Average quantity of food claimed per receiver':df_13,
    'Most claimed meal type':df_14,
    'Total quantity of food donated by each provider':df_15
    
}

selected_dfs_1 = st.selectbox("Select Table",list(dataframes_1.keys()))

st.dataframe(dataframes_1[selected_dfs_1])