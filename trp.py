import requests
from markdownify import markdownify
from bs4 import BeautifulSoup
import re

TRP_URL = "https://fabtcg.com/resources/rules-and-policy-center/tournament-rules-and-policy/"
r = requests.get(TRP_URL)
r.raise_for_status()

soup = BeautifulSoup(r.content, 'html.parser')
content = soup.find('div', class_='page-content')
md = markdownify(str(content))

# Fix section headers
md = re.sub(r'#(#+)', r'\1', md)

# Create section anchor links
md = re.sub(r'^(#+) (\d[.\d\w]*?)\.? (.+?)$',
            r'\1 \2 \3 <a href="#\2" id="\2">#</a>',
            md,
            flags=re.M,
)

# Fix extra whitespace in tables
md = re.sub(r'\|\s{2,}(.+?)\s+(?=\|)',
            r'| \1 ',
            md,
            flags=0,
)

# No newlines in links
md = re.sub(r'\n(?=[^\[]+\])', '', md)

# Collapse whitespace
md = re.sub(r'[ \t]+', ' ', md)
md = re.sub(r'\n\n+', '\n\n', md)

# Should be a link to fabtcg
md = re.sub(r'(\[.+?\]\()(\/.+?\))',
            r'\1https://fabtcg.com\2',
            md,
            flags=0,
)

with open('trp.md', 'w') as f:
    f.write(f"Flesh and Blood Tournament Rules and Policy, courtesy of Legend Story Studios.\n\n")
    f.write(f"Original available at [{TRP_URL}]({TRP_URL})\n\n")
    f.write(md)
