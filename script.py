import catalog_suffix_fixer as c
import multiprocessing
import os

mypath = 'catalog_suffix_fixer/input/'

if __name__ == "__main__":
    # start logging
    c.log.log_start()
    # initialize monitor tasks for each subfolder
    for subdir in os.listdir(mypath):
        # initialize monitors
        multiprocessing.Process(target=c.veranus.start_monitor, args=(f"{mypath}{subdir}/", )).start()
        # log monitor task started
