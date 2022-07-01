# Extraction
from bs4 import BeautifulSoup
import urllib3
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
http = urllib3.PoolManager(100)
urllib3.disable_warnings()
raw_site = "http://www.eitc.irs.gov/eitc-central/participation-rate/eitc-participation-rate-by-states"
site = http.request('GET', raw_site, headers=hdr).data

soup = BeautifulSoup(site)
table = soup.find('table', attrs={'class':'table'})
table_rows = table.find_all('tr')
df = pd.read_html(str(table))[0]

#################################
#################################
# Static Map
df.columns = df.columns.str.replace('Tax Year ', '')
df.columns = df.columns.str.replace('Participation Rate by State', 'state')
df = df.replace("%","", regex=True)

for y in df.columns :
    if y.startswith("2") :
        df[y] = pd.to_numeric(df[y])/100

# State name to abbreviation
df["state"] = df["state"].apply(lambda name : name.title())
import geopandas as gpd
import matplotlib.pyplot as plt
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
df["state"] = df["state"].str.replace(' Of ', ' of ')    
# invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))
df['abbrev'] = df['state'].map(us_state_to_abbrev)

from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected = True)
import plotly.express as px

fig = px.choropleth(df,
                    locations='abbrev', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='2014',
                    color_continuous_scale="Viridis_r",          
                    )
fig.show()

#################################
#################################
# Dynamic map
df2 = df
df2 = pd.melt(df , id_vars = "abbrev" , value_vars = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"])
df2['variable'] = pd.to_datetime(df2['variable']).dt.year.astype(str)
df2=df2.sort_values("variable") # Make sure you sort the time horizon column in ascending order because this column is in random order in the raw dataset
df2 = df2.rename(columns = {"variable": "Year" , "value" : "eitc"})
# df2["eitc"].describe()

#https://stackoverflow.com/questions/63094039/plotly-express-can-you-manually-define-legend-in-px-choropleth
#https://stackoverflow.com/questions/62795331/python-can-i-make-the-colorbar-static-in-a-plotly-time-series-choropleth
import plotly.express as px
fig = px.choropleth(df2,
                    locations='abbrev', 
                    locationmode="USA-states", 
                    color='eitc',
                    color_continuous_scale="Viridis_r", 
                    scope="usa",
                    animation_frame='Year')

fig.update_layout(
    title_text = 'EITC Participation Rate by State',
    title_font_family="Times New Roman",
    title_font_size = 22,
    title_font_color="black",
    title_x=0.45,
    range_color=[min(df2.eitc), max(df2.eitc))] ,
    #zmin=0.7,
    #zmax=0.86,
    coloraxis_colorbar=dict(
    title="Rate" ,
    #ticks="outside",
    #tickvals=[0.7,0.74,0.78,0.80,0.82],
    )
         )
fig.show()

