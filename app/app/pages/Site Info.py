import streamlit as st
import requests, json
import pandas as pd
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
def get_site_name_df() -> pd.DataFrame:
  sites = req.get_site_names()
  df = pd.DataFrame(sites)
  return df

@st.cache_data
def get_site_info(site:str)-> str:
  info = req.get_documents_by_site(site)
  return info['site_markdown']



site_name_df = get_site_name_df()

full_site_name = st.selectbox("Sites",site_name_df['full_name'])
if full_site_name is not None:
  site_id = site_name_df.query(f"full_name == '{full_site_name}'")["site_id"].values[0]
  if site_id is not None:
    st.markdown(get_site_info(site_id))
