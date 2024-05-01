from flask import Flask, jsonify, render_template, send_from_directory
import json
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import geopandas as gpd
import plotly
import plotly.express as px
import json
from flask import request

# Define the file path
file_path_2 = 'crimes_covid.csv\\part-00000-f8910cea-443b-4b72-bd93-617b172cdb6e-c000.csv'

# Read the CSV file into a Pandas DataFrame
crimes_covid = pd.read_csv(file_path_2)
crimes_covid = crimes_covid.dropna()
crimes_covid['Community_Area'] = crimes_covid['Community_Area'].astype(int)

# Load shapefile
gdf = gpd.read_file('shapefile\geo_export_b5ad3c27-d634-493d-b1fb-a8dc483237e3.shp')
gdf['area_num_1'] = gdf['area_num_1'].astype(int)
crime_counts = crimes_covid.groupby('Community_Area').size().reset_index(name='Crime_Count')
gdf = gdf.merge(crime_counts, how='left', left_on='area_num_1', right_on='Community_Area')

crimes_covid_2 = crimes_covid
crime_count_2 = crimes_covid_2.pivot_table(index='Community_Area', columns='Year', aggfunc='size', fill_value=0)
crime_count_2.reset_index(inplace=True)
crime_count_2.columns.name = None  # Remove the column name created by pivot_table
crime_count_2.columns = ['Community_Area'] + ['Crime_Count_' + str(year) for year in crime_count_2.columns[1:]]

gdf_with_crime = gdf.merge(crime_count_2, on='Community_Area', how='left')
gdf_with_crime.fillna(0, inplace=True)

def generate_choropleth_2(dataframe, year):
    color_column = f"Crime_Count_{year}"
    fig = px.choropleth(dataframe,
                        geojson=json.loads(dataframe.geometry.to_json()),  # Convert geometry to GeoJSON
                        locations=dataframe.index,  # Ensure this is correct
                        color=color_column,
                        color_continuous_scale="OrRd",
                        labels={color_column: 'Number of Crimes'}
                        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title={'text': f"Crime Frequency in Chicago by Community Area in {year}", 'x': 0.5, 'xanchor': 'center'})
    return fig

crimes_covid['Date'] = pd.to_datetime(crimes_covid['Date'])
daily_crime_counts = crimes_covid.groupby(crimes_covid['Date'].dt.date).size().rename('Crime_Count')
daily_crime_counts_df = daily_crime_counts.reset_index()
daily_crime_counts_df.rename(columns={'index': 'Date'}, inplace=True)
daily_crime_counts_df['Date'] = pd.to_datetime(daily_crime_counts_df['Date'])
daily_crime_counts_df['Year'] = daily_crime_counts_df['Date'].dt.year

def generate_time_series(dataframe, year):
    # Filter dataframe for the specified year
    filtered_df = dataframe[dataframe['Date'].dt.year == year]
    
    # Create the plot
    fig = px.line(filtered_df, x='Date', y='Crime_Count',
                  title=f'Daily Crime Occurrences Over Time in {year}',
                  labels={'Crime_Count': 'Number of Crimes', 'Date': 'Date'})
    fig.update_traces(mode='lines+markers')
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))  # Update layout if needed
    
    return fig

frequency = pd.DataFrame(crimes_covid.value_counts(['Primary_Type', 'Year']))
frequency.reset_index(inplace=True)
frequency.columns.name = None
frequency.columns = ['Primary_Type', 'Year', 'Crime_Count']

def generate_bar_plot(dataframe, year):
    # Filter dataframe for the specified year
    filtered_df = dataframe[dataframe['Year'] == year]
    
    # Create the plot
    fig = px.bar(filtered_df.head(11), x='Primary_Type', y='Crime_Count',
             title='Frequency of Primary Crime Type',
             labels={'count':'Frequency', 'Primary_Type':'Primary Type'})
    fig.update_traces(marker_color='indianred')
    
    return fig

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard2.html')

@app.route('/data/choropleth', methods=['GET'])
def choropleth_data():
    year = int(request.args.get('year', default=2020))  # Convert year to integer
    fig = generate_choropleth_2(gdf_with_crime, year)  # Call your function to create the plot
    return fig.to_json()  # Return the figure as JSON directly

@app.route('/data/line', methods=['GET'])
def line_data():
    year = int(request.args.get('year', default=2020))  # Convert year to integer
    fig = generate_time_series(daily_crime_counts_df, year)  # Call your function to create the plot
    return fig.to_json()  # Return the figure as JSON directly

@app.route('/data/bar', methods=['GET'])
def bar_data():
    year = int(request.args.get('year', default=2020))  # Convert year to integer
    fig = generate_bar_plot(frequency, year)  # Call your function to create the plot
    return fig.to_json()  # Return the figure as JSON directly

if __name__ == '__main__':
    app.run(debug=True, port = 5004)