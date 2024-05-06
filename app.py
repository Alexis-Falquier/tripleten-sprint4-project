import pandas as pd
import streamlit as st
import plotly.express as px

#START DATA CLEANUP AND ENHANCEMENT

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
#remove mercedes-benz
df_vehicles.query('make != "mercedes-benz"',inplace=True)
#drop rows with empyt model year values
df_vehicles.dropna(subset=['model_year'],inplace=True)
df_vehicles['model_year'] = df_vehicles['model_year'].astype("int")

#fill missing values for cylinders paint color and odometer:

#function to find the mode:
def get_mode(series):
    mode_val = series.mode()
    if not mode_val.empty:
        return mode_val.iloc[0]
    return None

# cylinder averages by 'model' and 'model_year'
cyl_avg = df_vehicles.groupby(['model', 'model_year']).agg({
    'cylinders': get_mode,
}).reset_index()
# cylinder averages by model
cyl_avg_by_model = df_vehicles.groupby(['model']).agg({
    'cylinders': get_mode,
}).reset_index()

#aggregate the cylinder averages:
cyl_avg = cyl_avg.merge(cyl_avg_by_model, on=['model'], how='left', suffixes=('', '_by_model'))
#fill the missing cylinder values of the model model_year pairs with the model averages
cyl_avg['cylinders'] = cyl_avg['cylinders'].fillna(cyl_avg['cylinders_by_model'])

#aggregate the paint color averages:
#paint color averages by model
paint_avg = df_vehicles.groupby(['model']).agg({
    'paint_color': get_mode,
}).reset_index()
#merge into cylinder average dataframe
paint_cyl_averages = cyl_avg.merge(paint_avg, on=['model'], how='left')
#drop extra cylinder column
paint_cyl_averages.drop(['cylinders_by_model'], axis=1, inplace=True)

#aggreage odometer averages:
#means of odometer readings by condition and by year
odo_by_condition = df_vehicles.groupby(['condition']).agg({
    'odometer': 'mean',
}).reset_index()

odo_by_year = df_vehicles.groupby(['model_year']).agg({
    'odometer': 'mean',
}).reset_index()

#aggregate all averages into the df_vehicles data frame
df_vehicles = df_vehicles.merge(paint_cyl_averages, on=['model','model_year'], how='left', suffixes=('', '_avg'))
df_vehicles = df_vehicles.merge(odo_by_condition, on=['condition'], how='left', suffixes=('', '_avg_by_condition'))
df_vehicles = df_vehicles.merge(odo_by_year, on=['model_year'], how='left', suffixes=('', '_avg_by_year'))
#make an average odometer column based on the average by year and condition
df_vehicles['odometer_avg'] = df_vehicles[['odometer_avg_by_condition', 
                                           'odometer_avg_by_year'
                                          ]].mean(axis=1)
#drop extra columns
df_vehicles.drop(['odometer_avg_by_condition',
                  'odometer_avg_by_year'
                 ], axis=1, inplace=True)

#replace missing values in the dataframe with the averages for cylinders odometer and paint color
for column in ['cylinders', 'odometer', 'paint_color']:
    df_vehicles[column] = df_vehicles[column].fillna(df_vehicles[f'{column}_avg'])
    
#drop average columns:
df_vehicles.drop([col for col in df_vehicles.columns if '_avg' in col], axis=1, inplace=True)

#cleanup columns types
df_vehicles['odometer'] = df_vehicles['odometer'].round().astype(int)
df_vehicles['cylinders'] = df_vehicles['cylinders'].astype(int)

#END DATA CLEANUP AND ENHANCEMENT

#STREAMLIT APP CODE

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
    index=comparison_list.index('none')
)

#checkbox if a user wants to normalize the histogram
normalize = st.checkbox('normalize histogram', value=False)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

if comparison == 'none':
    fig=px.histogram(
        df_vehicles,
        title='Histogram of Odometer Reading Frequency',
        x='odometer',
        nbins=100,
        histnorm=histnorm
    )
else:
    fig=px.histogram(
        df_vehicles,
        title=f'Histogram of Odometer Reading Frequency per Vehicle {comparison}',
        x='odometer',
        color=f'{comparison}',
        nbins=100,
        histnorm=histnorm
    )
fig.update_layout(xaxis_title='Odometer Reading',yaxis_title='Number of Vehicles')
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