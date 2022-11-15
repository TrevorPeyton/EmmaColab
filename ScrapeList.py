from PIL import Image
import tesserocr
from pdf2image import convert_from_path
import pandas as pd
import os
import json
def scrape_from_list(path, save_path, l, procnum):
    total = len(l)
    for current_slice, slice in enumerate(l):
        print(f"Process {procnum} - batch {current_slice} out of {total}")
        full_pages = {}
        skipped_files = []
        sub_total = len(slice)
        api = tesserocr.PyTessBaseAPI()
        for n, item in enumerate(slice):
            pages = []
            try:
                print(f"Process {procnum} - file {n+1} out of {sub_total} ------------ starting pdf2img")
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
                print(f"Process {procnum} - file {n+1} out of {sub_total} ------------ starting page scrape")
                for page_number, page_data in enumerate(images):
                    api.SetImage(page_data)
                    txt = str(api.GetUTF8Text()).lower().replace(' ', '')
                    if 'item20' in txt:
                        pages.append([page_number -1, page_number, page_number +1])
                if len(pages) == 0:
                    skipped_files.append(item)
                    print(f"Process {procnum} - file {n+1} out of {sub_total} ------------ no pages found")
                else:
                    full_pages[item] = pages
                    print(f"Process {procnum} - file {n+1} out of {sub_total} ------------ {pages} found")
            except:
                skipped_files.append(item)
                print(f"Process {procnum} - file {n+1} out of {sub_total} ------------ failed to scrape")
            
            n += 1
    
    with open(os.path.join(save_path, f"skipped-{current_slice}"), "w") as fp:
        json.dump(skipped_files, fp)
    with open(os.path.join(save_path, f"full-{current_slice}"), "w") as fp:
        json.dump(skipped_files, fp)