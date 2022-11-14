from sre_constants import SUCCESS
from atlassian import Confluence
import os
from bs4 import BeautifulSoup
import pandas as pd
import json
import yaml
from pprint import pprint

user = "**"
password = "**"
server = "https://confluence.menshovv.ru/"

confluence = Confluence(url=server, username=user, password=password, verify_ssl=False)
page = confluence.get_page_by_title("HRTECH", "Scale", expand="body.storage")
body = page["body"]["storage"]["value"]

tables_raw = [[[cell.text for cell in row("th") + row("td")]
                    for row in table("tr")]
                    for table in BeautifulSoup(body, features="lxml")("table")]

tables_df = [pd.DataFrame(table) for table in tables_raw]
for table_df in tables_df:
    print(table_df)

result = table_df.to_json(orient='split',index=False,indent=4)
parsed = json.loads(result)
json.dumps(parsed, indent=4)  
wiki_repl = int(parsed.get('data')[3][2][0])

print(parsed.get('data')[3][2][0])

with open('/Users/19689700/ci03189741_quality_gate/projects-config.yaml') as f:
    templates = yaml.safe_load(f)


bb_repl = int(templates.get('analytics-constructor')['environment']['PROM']['resources']['replicas'])
print(bb_repl)
print(wiki_repl+bb_repl)

if bb_repl >= wiki_repl:
    print('SUCCESS')
else:
    print('Колличество реплик меньше чем требуется сервису. Текущее колличество реплик -', bb_repl,'Требуемое колличество реплик -', wiki_repl )
    exit("'Колличество реплик меньше чем требуется сервису'")