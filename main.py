import httpx
from selectolax.parser import HTMLParser

# Define the target URL and headers
url = "https://example.com"
headers = {"User-Agent":""}

# Get and parse the webpage
response = httpx.get(url, headers=headers)
if response.status_code == 200:
    html = HTMLParser(response.text)
    content = html.body.html
    print(content)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")