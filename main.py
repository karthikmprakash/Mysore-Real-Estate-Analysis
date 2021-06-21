import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import time
import numpy as np
import pickle
import json
from sklearn.ensemble import RandomForestRegressor
import altair as alt

with open('locations.json','r') as f:
    location = json.load(f)



with open('mysore_home_prices_model.pickle', 'rb') as f:
            model = pickle.load(f)

with open("columns.json", "r") as f:
    data_columns = json.load(f)['data_columns']
    

def predict_price(location,ppsqft,area,beds):    
    loc_index = data_columns.index(location)
    beds_index = data_columns.index(beds)
    
    x = np.zeros(len(data_columns))
    #x[0] = beds
    x[0] = area
    x[1] = ppsqft
    
    if loc_index >= 0:
        x[loc_index] = 1
    if beds_index >= 0:
        x[beds_index] = 1

    return model.predict([x])[0]

@st.cache
def load_data():
    data = pd.read_csv('combined_cleaned.csv')
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")
location_list = list(location.keys())
location_list.append('None')


## Sidebar code
cities_filter = st.sidebar.multiselect('Select 2 more locaitons for price comparision', location_list)
if cities_filter:
    loc_select = st.sidebar.selectbox("Select the location",location_list,index=location_list.index(cities_filter[0]))
else:
     loc_select = st.sidebar.selectbox("Select the location",location_list,index=location_list.index('None'))
beds_select = st.sidebar.slider('Number of Beds', 1,8)    


# main page code
st.markdown(""" <h1 align="center"> House Price Prediction - Mysore </h1>""",unsafe_allow_html=True)


if loc_select != 'None':
    predicted_price = round(predict_price(loc_select,location[loc_select],(500*beds_select)+500,beds_select),2)
    if predicted_price >= 100:
        st.markdown(f""" Approximate price of house in `{loc_select}` with `{beds_select}` beds is """,unsafe_allow_html=True)
        st.markdown(f""" <h2 align="center" style= "color:rgb(14, 17, 23); background-color:white"> &#8377;{round(predicted_price/100,2)} Crores</h2>""",unsafe_allow_html=True)
    else:
        st.markdown(f""" Approximate price of house in `{loc_select}` with `{beds_select}` beds is """,unsafe_allow_html=True)
        st.markdown(f""" <h2 align="center" style= "color:rgb(14, 17, 23); background-color:white"> &#8377;{predicted_price} Lakhs</h2>""",unsafe_allow_html=True)




chart = alt.Chart(data).mark_bar().encode(
    x='Location',
    y=('average(Price)')
)

#st.altair_chart(chart)


import matplotlib.pyplot as plt
plt.style.use('dark_background')
import seaborn as sns


def avg_price(location):
    price_list=[]
    no_price_list = []
    location_list = []
    avg_loc_bed = data.groupby(['Location','Beds'])['Price'].mean()
    
    for x in location:
        try:
            price_list.append(avg_loc_bed[x][int(beds_select)])
            location_list.append(x)
        except KeyError:
            no_price_list.append(x)

    if len(no_price_list) >= 1:
        st.warning(f'Unfortunately, there are no data avaialbe for {beds_select} beds in {no_price_list} locations ')
    return price_list,location_list

fig, ax = plt.subplots()
if len(avg_price(cities_filter)[1]) > 1:
    ax.bar(avg_price(cities_filter)[1],avg_price(cities_filter)[0],color = ['#f63366','c'])
    plt.title('Average price comparision for selected locations')
    plt.ylabel('Price in Lakhs')
    plt.xticks(rotation=45)
    plt.xlabel('Location Names')
    st.pyplot(fig)