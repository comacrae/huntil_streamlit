import streamlit as st
import pandas as pd
import requests
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

@st.cache_data
def get_harvest_df():
  return pd.DataFrame(req.get_harvest())

@st.cache_data
def get_options(harvest_df):
  site_options = sorted(harvest_df['site'].unique())
  years_options = sorted(harvest_df['year'].unique())
  species_options = sorted(harvest_df['species'].unique())
  seasons_options = sorted(harvest_df['season'].unique())
  subcategory_options = sorted(harvest_df['subcategory'].unique())
  return site_options, years_options, species_options, seasons_options, subcategory_options

@st.cache_data
def filter_df(df, site_option, species_options):
  df = df[df['site'] == site_option]
  df = df[df['species'] == species_options]
  return df


harvest_df = get_harvest_df()
site_options, years_options, species_options, seasons_options, subcategory_options = get_options(harvest_df)

st.title("Harvest Data")

with st.form("harvest_form"):
  col1,col2 = st.columns(2)
  with col1: 
    sites= st.selectbox(label="Site",options=site_options)
  with col2:
    species = st.selectbox(label="Species",options=species_options)
  submit = st.form_submit_button(label="Filter Data")

if submit:
  filtered_df = filter_df(harvest_df,sites,species)
  if filtered_df.empty:
    st.error("No data matches given filters")
  else:
    st.dataframe(data=filtered_df, hide_index=True)
    output_df = filtered_df[["site","species","year", "harvest_count"]]
    st.bar_chart(data=output_df, x="year",x_label="Year", y="harvest_count", y_label="Annual Harvest Count")
