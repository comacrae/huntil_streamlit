import streamlit  as st
import pandas as pd
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests, json
class Requester:
  def __init__(self, base_url:str="https://hunt-il-backend-fd6fc52c0ba0.herokuapp.com/api/")-> list:
    self.base_url = base_url
  
  def get_and_parse(self,url,params=None):
    res = requests.get(url,params=params)
    if(res.ok):
      return res.json()
    else:
      raise Exception("HTTP Code: ", res.status_code, res.content)
  
  def get_paginated_response(self, url:str) ->list:
    full_list = []
    offset = 0
    res_list = self.get_and_parse(url, params={'offset':offset,'limit':100})
    while len(res_list) > 0:
      full_list += res_list
      offset += 100
      res_list = self.get_and_parse(url, params={'offset':offset,'limit':100})
    return full_list

  def get_site_names(self)-> list:
    url = self.base_url + 'sites/names'
    return self.get_paginated_response(url)

  def get_site_name_info(self,site_id:str) ->dict:
    url = self.base_url + f"sites/{site_id}/names"
    return self.get_and_parse(url)
  
  def get_huntable_species(self) -> list:
    url = self.base_url + 'huntable-species/'
    return self.get_paginated_response(url)
  
  def get_huntable_species_by_site(self, site_id:str) -> dict:
    url = self.base_url + f"huntable-species/site/{site_id}"
    return self.get_and_parse(url)

  def get_sites_by_huntable_species(self, species:str) -> dict:
    url = self.base_url + f"huntable-species/species/{species}"
    return self.get_and_parse(url)
  
  def get_geography(self) -> list:
    url = self.base_url + f"geography/"
    return self.get_and_parse(url)

  def get_geography_by_site(self, site_id:str) -> dict:
    url = self.base_url + f"geography/{site_id}"
    return self.get_and_parse(url)

  def get_documents(self) -> list:
    url = self.base_url + f"documents/"
    return self.get_and_parse(url)

  def get_documents_by_site(self, site_id:str) -> dict:
    url = self.base_url + f"documents/{site_id}"
    return self.get_and_parse(url)

  def get_harvest(self) -> list:
    url = self.base_url + f"harvest/"
    return self.get_paginated_response(url)


req = Requester()


def get_map(df, address_coords):

  df['radius'] = 3000
  layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position="[longitude, latitude]",
    get_fill_color=[255, 0, 0],  # Red color with some transparency
    get_radius = "radius",
    pickable=True,  # Enables tooltips
  )
  tooltip = {
    "html": "<b>{full_name}</b><br><b>Huntable Acres:</b> {huntable_acres}<br><b>Species:</b> {species}",
    "style": {"backgroundColor": "white", "color": "black"},
  }

  view_state = pdk.ViewState(
    latitude=address_coords[0],
    longitude=address_coords[1],
    zoom=7,
    pitch=0
  )

  m = pdk.Deck(
      layers=[layer],
      initial_view_state=view_state,
      tooltip=tooltip,
      map_style="light"
  )
  return m


@st.cache_data
def get_site_names():
  res = req.get_site_names()
  return pd.DataFrame(res)

@st.cache_data
def get_huntable_species_df_by_site(site_id:str):
  res = req.get_huntable_species_by_site(site_id)
  return pd.DataFrame(res)

@st.cache_data
def get_huntable_species_df():
  res = req.get_huntable_species()
  return pd.DataFrame(res)

@st.cache_data
def get_geography_df() -> pd.DataFrame:
  res = req.get_geography()
  df = pd.DataFrame(res)
  return df

@st.cache_data
def get_merged_df(geo:pd.DataFrame, huntable:pd.DataFrame) -> pd.DataFrame:
  return pd.merge(geo,huntable, on="site_id", how="left")



@st.cache_data
def get_coords(address:str) -> tuple:
  illinois_bounding_box = [(36.97,-91.51), (42.50, -87.02)] 
  if "IL" in address:
    coded = geolocator.geocode(address, viewbox=illinois_bounding_box, bounded=True)
  else:
    coded = geolocator.geocode(address)
  return coded.latitude, coded.longitude

@st.cache_data
def calc_distance( df:pd.DataFrame,max_distance:int,coords:tuple) -> pd.DataFrame:
  if df.empty:
    return df
  df['distance'] = df.apply(lambda x: geodesic((x['latitude'], x['longitude']),coords).miles,axis=1)
  df = df[df['distance'] <= max_distance]
  return df


@st.cache_data
def filter_geo_df(geo_df:pd.DataFrame, min_acrage:int,counties:list=None):
  geo_df = geo_df[geo_df['huntable_acres'] >= min_acrage]
  if counties is not None and counties != []:
    geo_df = geo_df[geo_df['county'].isin(counties)]
  return geo_df

@st.cache_data
def filter_huntable_df(huntable_df:pd.DataFrame,species:list = None,seasons:list = None ):
  if species is not None and species != []:
    huntable_df = huntable_df[huntable_df['species'].isin(species)]
  if seasons is not None and seasons != []:
    huntable_df = huntable_df[huntable_df['season'].isin(seasons)]
  return huntable_df

@st.cache_data
def get_sorted_options(huntable_df, geo_df):
  species_options = sorted(huntable_df['species'].unique())
  season_options = sorted(huntable_df['season'].unique())
  counties_options = sorted(geo_df['county'].unique())
  return species_options, season_options, counties_options



geolocator = Nominatim(user_agent="huntil_backend_streamlit")
geo_df = get_geography_df()
huntable_df = get_huntable_species_df()
site_names_df = get_site_names()
species_options, season_options, counties_options = get_sorted_options(huntable_df, geo_df)



st.title("Nearest Hunting Locations")

with st.form("location_form"):
  address = st.text_input(label="Address", placeholder="123 Main Street, Chicago, IL")
  col1,col2 = st.columns(2)
  col3,col4, col5 = st.columns(3)
  with col1: 
    seasons= st.multiselect(label="Seasons",options=season_options, default=None)
  with col2:
    species = st.multiselect(label="Species",options=species_options, default=None)
  with col3:
    counties = st.multiselect(label="Counties",options=counties_options, default=None)
  with col4:
    min_acrage = st.number_input(label="Min Huntable Acres", min_value=1,max_value=300000, value=1, step=100)
  with col5:
    max_distance = st.number_input(label="Max Miles From Address", max_value=400, min_value=0, value=100, step=10)
  submit = st.form_submit_button(label="Find Closest Sites")

if submit:
  try:
    addr_coords = get_coords(address)
    st.write(f"Geocoded coordinates: {addr_coords}")
  except Exception as e:
    st.error("Unable to get coordinates. Make sure you're using a full street address, city, and state.")
  filtered_geo_df = filter_geo_df(geo_df, min_acrage=min_acrage,counties=counties)
  if filtered_geo_df.empty:
    st.error("No sites exist with given minimum acrage and county selections.")
  else:
    filtered_huntable_df = filter_huntable_df(huntable_df, species=species, seasons=seasons)
    if filtered_huntable_df.empty:
      st.error("No sites exist with given species and season selections.")
    else:
      filtered_geo_df= calc_distance(filtered_geo_df, max_distance=max_distance, coords=addr_coords)
      merged_df = pd.merge(filtered_geo_df, filtered_huntable_df, on="site_id", how="left")
      merged_df = pd.merge(merged_df,site_names_df, on="site_id", how="left")
      if merged_df.empty:
        st.error("No sites exist within maximum distance that match given selections.")
      else:
        map_df = merged_df.groupby(['distance','full_name','region','county','address','huntable_acres', 'latitude','longitude'])['species'].unique().agg(list).reset_index()
        m = get_map(map_df, addr_coords)
        st.dataframe(data=map_df[["distance","full_name","region","county","address","huntable_acres","species"]],hide_index=True)
        st.pydeck_chart(m)
