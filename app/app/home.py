import streamlit as st

st.title("Hunt IL Site Finder")

# This data is *not* up to date. Please 
## About
st.header("Warning: This site is a portfolio project and does not accurately reflect Illinois' hunting site regulation or laws. Please visit [HuntIL](https://huntillinois.org/) for sanctioned information.")
st.markdown("""

This is a Streamlit front-end that allows users to interact with a scraped/cleaned SQLite respository of Illinois hunting locations.
I decided to create this after spending way too much time cross-referencing resources trying to answer the simple question:
***"What are the closest N places from my address that I can hunt X,Y, and Z?"***

There are three tabs:

### Nearest Location
Allows you to enter your address and uses the coordinates of sites to determine which sites are closest that match your preferences.
### Site Info
Displays the webscraped pages of the Hunt IL website for each hunting location in Markdown.
### Harvest Data
Displays all the harvest data I was able to obtain from IDNR record requests and an exposed API endpoint.
**Please note that there's a lot of data and I'm using a free Heroku instance to host my API, so this page takes a while to load**
""")
