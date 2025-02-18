import requests, json
import pandas as pd
class Requester:
  def __init__(self, base_url:str="https://hunt-il-backend-fd6fc52c0ba0.herokuapp.com/api/")-> list:
    self.base_url = base_url
  
  def get_and_parse(self,url):
    res = requests.get(url)
    if(res.ok):
      return res.json()
    else:
      raise Exception("HTTP Code: ", res.status_code)

  def get_site_names(self)-> list:
    url = self.base_url + 'sites/names'
    return self.get_and_parse(url)
      
  def get_site_name_info(self,site_id:str) ->dict:
    url = self.base_url + f"sites/{site_id}/names"
    return self.get_and_parse(url)
  
  def get_huntable_species(self) -> list:
    url = self.base_url + 'huntable-species/'
    return self.get_and_parse(url)
  
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
    return self.get_and_parse(url)


  