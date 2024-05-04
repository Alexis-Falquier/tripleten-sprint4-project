import pandas as pd
import scipy.stats
import streamlit as st
import plotly.express as px

#reading in the data
df_vehicles = pd.read_csv("./vehicles_us.csv")
#cleaning up null values
df_vehicles['is_4wd'].fillna(0,inplace=True)
df_vehicles['is_4wd'] = df_vehicles['is_4wd'].astype("int")
#making "make" column
df_vehicles['make'] = df_vehicles['model'].str.split().str[0]
cols = df_vehicles.columns.tolist() 
cols.insert(2, cols.pop(cols.index('make')))
df_vehicles = df_vehicles[cols]


st.title('A brief analysis of vehicle odometer readings')
st.text('''Below you will find a few different graphs and charts to play with 
comparing the odometer readings of vehicles against other vehicle metrics. 
The data pertains to used vehicles sold in the US.''')


st.header('Compare odometer reading and price of a vehicle sold by vehicle make')
# get a list of car makes/models
make_list = sorted(df_vehicles['make'].unique())
model_list = sorted(df_vehicles['model'].unique())
# get user's inputs from a dropdown menu
make = st.selectbox(
    label='Select make', # title of the select box
    options=make_list, # options listed in the select box
    index=make_list.index('acura') # default pre-selected option
    )

one_vehicle = df_vehicles.query(f"make == '{make}'")
fig = px.scatter(
    one_vehicle,
    title=f'Price vs Odometer Reading of {make} Cars',
    y='price',
    x='odometer'
)
fig.update_layout(xaxis_title='odometer reading',yaxis_title='price ($ USD)')
st.write(fig)


st.header('Compare odometer reading and price of a vehicle sold by vehicle model')
# get a list of car makes/models
model_list = sorted(df_vehicles['model'].unique())
# get user's inputs from a dropdown menu
model = st.selectbox(
    label='Select make', # title of the select box
    options=model_list, # options listed in the select box
    index=model_list.index('acura tl') # default pre-selected option
    )

one_vehicle = df_vehicles.query(f"model == '{model}'")
fig = px.scatter(
    one_vehicle,
    title=f'Price vs Odometer Reading of {model} Cars',
    y='price',
    x='odometer'
)
fig.update_layout(xaxis_title='odometer reading',yaxis_title='price ($ USD)')
st.write(fig)


st.header('Histogram viewing frequency of odometer readings')
st.subheader('make comparisons of odometer reading frequency accross different aspects of the vehicles')

comparison_list = [
    'none',
    'condition',
    'cylinders',
    'is_4wd',
    'make',
    'paint_color',
    'transmission',
    'type',
    ]
comparison = st.selectbox(
    label='comparisons',
    options=comparison_list, 
    index=comparison_list.index('condition')
)

if comparison == 'none':
    fig=px.histogram(
        df_vehicles,
        title='Histogram of Odometer Reading Frequency',
        x='odometer',
        nbins=100
    )
else:
    fig=px.histogram(
        df_vehicles,
        title=f'Histogram of Odometer Reading Frequency per Vehicle {comparison}',
        x='odometer',
        color=f'{comparison}',
        nbins=100
    )
fig.update_layout(xaxis_title='odometer reading',yaxis_title='frequency')
st.write(fig)


st.header("Bar chart looking at the average odometer reading per different categories of the vehicles")

comparison_list_2 = [
    'condition',
    'cylinders',
    'is_4wd',
    'make',
    'model',
    'paint_color',
    'transmission',
    'type',
    ]
comparison_2 = st.selectbox(
    label='comparisons',
    options=comparison_list_2, 
    index=comparison_list_2.index('condition')
)
df_od_by_color = df_vehicles.groupby(comparison_2)['odometer'].mean()
fig=px.bar(
    df_od_by_color,
    title=f'Average Odometer Reading per Vehicle {comparison_2}'
)
fig.update_layout(showlegend=False, yaxis_title='average odometer reading')
st.write(fig)