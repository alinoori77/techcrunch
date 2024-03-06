import requests
from bs4 import BeautifulSoup

url ="https://techcrunch.com/wp-json/tc/v1/magazine?page=1&_embed=true&_envelope=true&categories=20429"

response = requests.get(url)

json_data = response.json()

for i in range(1):  
  ali = {"data" : json_data["body"][i]["date"],
         "link" :json_data["body"][i]["link"],
         "title" :json_data["body"][i]["title"].get("rendered"),
         "author" :json_data["body"][i]["yoast_head_json"].get("author"),
         "keywords" :json_data["body"][i]["yoast_head_json"].get("schema").get("@graph")[0].get("keywords"),
         "media URL" : json_data["body"][i]["yoast_head_json"].get("og_image")[0].get("url"),
         "category" :json_data["body"][i]["yoast_head_json"].get("schema").get("@graph")[0].get("articleSection"),

         }


  print(ali)

