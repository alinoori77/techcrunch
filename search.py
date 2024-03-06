import requests
from bs4 import BeautifulSoup



search_word="instagram"
for page in range(1,5):
    print(page)
    url = "https://search.techcrunch.com/search;_ylt={_ylt};_ylc={_ylc}?p={p}&fr2={fr2}&fr={fr}"

# Replace these values with your actual values
    params = {
        "_ylt": "AwrFF.b.5eZlq.0Ia9CnBWVH",
        "_ylc": "X1MDMTE5NzgwMjkxOQRfcgMyBGZyA3RlY2hjcnVuY2gEZ3ByaWQDbnhBb1lkcFRTT3FHcTRwelh0ZzJmQQRuX3JzbHQDMARuX3N1Z2cDOQRvcmlnaW4Dc2VhcmNoLnRlY2hjcnVuY2guY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAM2BHF1ZXJ5A3NwYWNleAR0X3N0bXADMTcwOTYzMTE3Mg--",
        "p": "spacex",
        "fr2": "sb-top",
        "fr": "techcrunch"
    }

# Format the URL using f-string
    formatted_url = url.format(**params)    


    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        titles = [i.text for i in soup.find_all("a", class_="fz-20 lh-22 fw-b")]
        authors = [i.text for i in soup.find_all("span", class_="mr-15")]

        print(titles)
        print(authors)