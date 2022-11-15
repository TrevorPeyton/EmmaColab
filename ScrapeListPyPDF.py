from PyPDF2 import PdfReader
import camelot
import pandas as pd
import os
def scrape_from_list(save_path, l, procnum):
    total = len(l)
    for n, item in enumerate(l):
        pages = []
        try:
            print(f"Process {procnum} - file {n+1} out of {total} ------------ starting page scrape")
            reader = PdfReader(item)
            for page_number, page in enumerate(reader.pages):
                txt = str(page.extract_text()).lower().replace(' ', '')
                if 'item20' in txt:
                    pages.extend([page_number -1, page_number, page_number +1])
            if len(pages) > 0:
                pages = list(set([page for page in pages if page > 0 and page < len(reader.pages)])) #unique and positive
                tables = camelot.read_pdf(item, pages=",".join([str(page) for page in pages]))
                filename = item.split("/")[-1][:-4] + "_____.csv"
                tables.export(os.path.join(save_path, filename), f="csv")

        except:
            print(f"Process {procnum} - file {n+1} out of {total} ------------ failed to scrape")
        finally:
            print(f"Process {procnum} - file {n+1} out of {total} ------------ finished")