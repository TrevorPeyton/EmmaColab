import pandas as pd
import PyPDF2
import re
from io import StringIO
import os
import io
import codecs
path = r'C:\Users\cll319\Desktop\files'

os.chdir(path)

n = 0
skipped_files = []
full_pages = {}
for item in os.listdir(path):
    name = item[:-9] #[name, year]
    year = item[-8:-4]

    os.system('cls')
    print(f"Reading {n}th file")
    pages = set()
    try:
        with open(item, "rb") as fh:
            buf = io.BytesIO(fh.read())
            pdf = PyPDF2.PdfFileReader(buf)
            for page in range(pdf.numPages):
                lines = [line for line in pdf.getPage(page).extractText().split("\n") if "Item 20" in line]
                if len(lines) > 0:
                    pages.update([page -1, page, page +1])
    except:
        skipped_files.append(item)
    finally:
        if len(pages) > 0:
            skipped_files.append(item)
        else:
            full_pages[item] = pages
    
    n += 1

path = r'C:\Users\cll319\Desktop'
os.chdir(path)

import json
with open("skipped_pages", "w") as fp:
    json.dump(skipped_files, fp)

with open("full_pages", "w") as fp:
    json.dump(full_pages, fp)

