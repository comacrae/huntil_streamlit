import streamlit as st
import pandas as pd
from app.api import Requester
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
