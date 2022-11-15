from PIL import Image
import pytesseract
import camelot
from pdf2image import convert_from_path
import pandas as pd
import os
import json
def scrape_from_list(save_path, l, procnum):
    total = len(l)
    for n, item in enumerate(l):
        pages = []
        try:
            print(f"Process {procnum} - file {n+1} out of {total} ------------ starting pdf2img")
            images = convert_from_path(pdf_path=item,
            dpi=100,
            fmt="jpeg",
            jpegopt={
                "quality": 40,
                "progressive": False,
                "optimize": False
            },
            hide_annotations=True,
            thread_count=8)
            print(f"Process {procnum} - file {n+1} out of {total} ------------ starting page scrape")
            for page_number, page_data in enumerate(images):
                txt = str(pytesseract.image_to_string(page_data)).lower().replace(' ', '')
                if 'item20' in txt:
                    pages.extend([page_number -1, page_number, page_number +1])
            if len(pages) > 0:
                pages = list(set([page for page in pages if page > 0 and page < len(images)])) #unique and positive
                tables = camelot.read_pdf(item, pages=",".join([str(page) for page in pages]))
                filename = item.split("/")[-1][:-4] + "_____.csv"
                tables.export(os.path.join(save_path, filename), f="csv")

        except:
            print(f"Process {procnum} - file {n+1} out of {total} ------------ failed to scrape")
        finally:
            print(f"Process {procnum} - file {n+1} out of {total} ------------ finished")