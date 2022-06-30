#from bs4 import BeautifulSoup
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
df.columns = df.columns.str.replace('Tax Year ', '')
df.columns = df.columns.str.replace('Participation Rate by State', 'state')
df = df.replace("%","", regex=True)

for y in df.columns :
    if y.startswith("2") :
        df[y] = pd.to_numeric(df[y])/100
        
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
    
# invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))
df['abbrev'] = df['state'].map(us_state_to_abbrev)
df["state"] = df["state"].str.replace(' Of ', ' of ')

import plotly.express as px

    fig = px.choropleth(df,
                    locations='abbrev', 
                    locationmode="USA-states", 
                    scope="usa",
                    color='2018',
                    color_continuous_scale="Viridis_r", 
                    
                    )
fig.show()
