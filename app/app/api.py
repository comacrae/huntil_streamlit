import requests, json
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
    url = self.base_url + f"/sites/{site_id}/names"
    return self.get_and_parse(url)


  