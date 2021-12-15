import time

import catalog_suffix_fixer as c
import multiprocessing
import os

mypath = 'catalog_suffix_fixer/input/'

if __name__ == "__main__":
    # start logging
    c.log.log_start()
    # initialize monitor tasks for each subfolder
    max_procs = 4  # spawn up to 4 watchers
    proc_count = 0
    for subdir in os.listdir(mypath):
        if proc_count < max_procs:
            # initialize monitors
            multiprocessing.Process(target=c.veranus.start_monitor, args=(f"{mypath}{subdir}/", )).start()
            proc_count += 1
            # log monitor task started
    time.sleep(0.5)
    c.veranus.queue_existing(mypath)
