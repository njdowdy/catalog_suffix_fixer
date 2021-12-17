import time
import catalog_suffix_fixer as c
import multiprocessing
import os

mypath = 'catalog_suffix_fixer/input/'
max_proc = 4  # spawn up to 4 watchers


def main(path: str, max_processors: int) -> None:
    # start logging
    c.log.log_start()
    # initialize monitor tasks for each subfolder
    proc_count = 0
    for subdir in os.listdir(path):
        if proc_count < max_processors:
            # initialize monitors
            multiprocessing.Process(target=c.veranus.start_monitor, args=(f"{path}{subdir}/",)).start()
            proc_count += 1
            c.log.log_watchdog_startup(to_watch=f"{path}{subdir}/")
    time.sleep(0.1)
    c.veranus.queue_existing(path)


if __name__ == "__main__":
    main(mypath, max_proc)
