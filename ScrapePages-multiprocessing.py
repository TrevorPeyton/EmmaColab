import ScrapeListPyPDF
import multiprocessing as mp
import time
import os
# split a list into evenly sized chunks
def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
def dispatch_jobs(data, job_number, save_path):
    total = len(data)
    chunk_size = total // job_number
    slice = chunks(data, chunk_size)
    jobs = []

    for i, s in enumerate(slice):
        j = mp.Process(target=ScrapeListPyPDF.scrape_from_list, args=(save_path, s, i))
        jobs.append(j)
    for j in jobs:
        j.start()

if __name__ == "__main__":
    num_workers = mp.cpu_count()
    path = "/Users/trevorpeyton/data/emma-pdfs"
    save_path = "/Users/trevorpeyton/Desktop/emma-pdf-runs"
    os.chdir(path)

    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            paths.append(os.path.join(root, file))
    
    finished_paths = []
    for root, dirs, files in os.walk(save_path):
        for file in files:
            finished_paths.append(os.path.join(root, file))
    finished_paths = list(set([path.split("_____")[0].split("/")[-1] for path in finished_paths if path.endswith(".csv")]))
    paths = [path for path in paths if path.split("/")[-1][:-4] not in finished_paths]

    dispatch_jobs(paths, num_workers, save_path)