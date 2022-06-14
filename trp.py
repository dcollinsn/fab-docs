import requests
from markdownify import markdownify
from bs4 import BeautifulSoup

TRP_URL = "https://fabtcg.com/resources/rules-and-policy-center/tournament-rules-and-policy/"
r = requests.get(TRP_URL)
r.raise_for_status()

soup = BeautifulSoup(r.content, 'html.parser')
content = soup.find('div', class_='page-content')
print(content)
md = markdownify(str(content))
with open('trp.md', 'w') as f:
    f.write(md)
