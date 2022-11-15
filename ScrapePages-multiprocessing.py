import ScrapeList
import multiprocessing as mp
import time
import os
# split a list into evenly sized chunks
def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
def dispatch_jobs(data, job_number):
    total = len(data)
    chunk_size = total // job_number
    slice = chunks(data, chunk_size)
    jobs = []

    for i, s in enumerate(slice):
        sub_slices = chunks(s, 1)
        j = mp.Process(target=ScrapeList.scrape_from_list, args=("/Users/trevorpeyton/data/emma-pdfs", "/Users/trevorpeyton/Desktop/emma-pdf-runs", sub_slices, i))
        jobs.append(j)
    for j in jobs:
        j.start()

if __name__ == "__main__":
    num_workers = mp.cpu_count()
    path = "/Users/trevorpeyton/data/emma-pdfs"
    os.chdir(path)

    data = []
    for root, dirs, files in os.walk(path):
        for file in files:
            data.append(os.path.join(root, file))

    dispatch_jobs(data, num_workers)