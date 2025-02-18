from app.api import Requester
import pandas as pd

req = Requester()
def test_site_names(): 
  body = req.get_site_names()
  df = pd.DataFrame(body)
  print(df)

def test_site_name_info(site_id): 
  body = req.get_site_name_info(site_id)
  df = pd.DataFrame(body)
  print(df)

if __name__ == "__main__":
  test_site_names()
  test_site_name_info("andersonlakesfwa")
