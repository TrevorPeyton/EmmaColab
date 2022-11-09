import pandas as pd
import PyPDF2
import re
from io import StringIO
import os
import io
import camelot
path = r'C:\Users\cll319\Desktop'

os.chdir(path)

full_pages = {}
with open('full_pages') as json_file:
    full_pages = json.load(json_file)

path = r'C:\Users\cll319\Desktop\files'
save_path = r'C:\Users\cll319\Desktop\tables'

n = 0
skipped_files = []
full_pages = {}
for item in os.listdir(path):
    if item not in full_pages:
        continue

    name = item[:-9] #[name, year]
    year = item[-8:-4]

    os.system('cls')
    print(f"Reading {n}th file")
    try:
        tables = camelot.read_pdf('foo.pdf', pages=','.join(str(s) for s in full_pages[item]))
        tables.export(f'{save_path}\{name}___{year}.csv', f='csv', compress=True)
    except:
        skipped_files.append(item)
    
    n += 1

path = r'C:\Users\cll319\Desktop'
os.chdir(path)

import json
with open("skipped_tables", "w") as fp:
    json.dump(skipped_files, fp)


