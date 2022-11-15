import pandas as pd
import PyPDF2
import re
from io import StringIO
import os
import io
import codecs
# path = r'C:\Users\cll319\Desktop\files'
path = "/Users/trevorpeyton/data/emma-pdfs"

os.chdir(path)

n = 0
skipped_files = []
full_pages = {}
for item in os.listdir(path):
    name = item[:-9] #[name, year]
    year = item[-8:-4]

    os.system('cls')
    pages = []
    try:
        with open(item, "rb") as fh:
            buf = io.BytesIO(fh.read())
            pdf = PyPDF2.PdfFileReader(buf)
            for page in range(pdf.numPages):
                os.system('cls')
                print(f"Reading {n}th file {page} page")
                text = pdf.getPage(page).extractText().lower().replace(' ', '')
                if 'item20' in text:
                    pages.append([page -1, page, page +1])
                    
                if len(pages) == 0:
                    skipped_files.append(item)
                else:
                    full_pages[item] = pages
    except:
        skipped_files.append(item)
    
    n += 1

path = "/Users/trevorpeyton/Desktop/emma-pdf-runs"
os.chdir(path)

import json
with open("skipped_pages", "w") as fp:
    json.dump(skipped_files, fp)

with open("full_pages", "w") as fp:
    json.dump(full_pages, fp)