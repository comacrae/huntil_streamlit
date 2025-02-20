import streamlit as st
import pandas as pd
from app.api import Requester

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
