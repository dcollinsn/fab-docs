import requests
from markdownify import markdownify
from bs4 import BeautifulSoup
import re

PG_URL = "https://fabtcg.com/resources/rules-and-policy-center/penalty-guidelines/"
r = requests.get(PG_URL)
r.raise_for_status()

soup = BeautifulSoup(r.content, 'html.parser')
content = soup.find('div', class_='page-content')
md = markdownify(str(content))

# Fix section headers
md = re.sub(r'^(\d\. .+?)\n=+\n',
            r'## \1\n',
            md,
            flags=re.M,
)
md = re.sub(r'#(#+)', r'\1', md)
md = re.sub(r'^(#+)\s+\*+(.+?)\*+',
            r'\1 \2',
            md,
            flags=re.M,
)

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

# Weird CSS stuff
md = re.sub(r'^\s*\..+?\{.+?\}\s*$', '', md, flags=re.S|re.M)

# Collapse whitespace
md = re.sub(r'[ \t]+', ' ', md)
md = re.sub(r'\n\n+', '\n\n', md)

# Should be a link to fabtcg
md = re.sub(r'(\[.+?\]\()(\/.+?\))',
            r'\1https://fabtcg.com\2',
            md,
            flags=0,
)

with open('pg.md', 'w') as f:
    f.write(f"Flesh and Blood Procedure and Penalty Guidelines, courtesy of Legend Story Studios.\n\n")
    f.write(f"Original available at [{PG_URL}]({PG_URL})\n\n")
    f.write(md)
