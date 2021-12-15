import time
import os
import re
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def start_monitor(to_watch: str = 'catalog_suffix_fixer/input/'):
    # setup and define event handler
    event_handler = PatternMatchingEventHandler("*", "", False, True)
    event_handler.on_created = on_created
    # create monitor
    observer = Observer()
    # define monitor parameters and link to event handler
    observer.schedule(event_handler, to_watch, recursive=True)
    # begin monitoring
    observer.start()
    try:
        while True:
            time.sleep(30)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.stop()
        observer.join()


def on_created(event):
    file = event.src_path
    filestub = '/'.join(file.split('/')[2:])
    print(f"{filestub} has been detected.")
    # do a thing
    #
    # check if file exists in output
    file_out = f"{file.replace('input', 'output')}"
    if os.path.exists(f"{file_out}"):
        while os.path.exists(f"{file_out}"):
            file_out = rename_duplicate_file(file_out)  # if it does, rename it
        file_out_stub = '/'.join(file_out.split('/')[2:])
        print(f"{filestub} exists in output directory. Renamed to: {file_out_stub}")
    # move to output
    os.makedirs('/'.join(file_out.split('/')[0:-1]), exist_ok=True)
    os.rename(f"{file}", file_out)
    print(f"{filestub} has been processed and moved to output!")


def rename_duplicate_file(filename: str):
    file = '.'.join(filename.split('.')[0:-1])
    ext = filename.split('.')[-1]
    suffix = re.search(r"\(([0-9]+)\)", file)
    if suffix:
        suffix_value = int(suffix.group(1))
        file = re.sub(rf"\({suffix_value}\)", f"({suffix_value + 1})", file)
    else:
        file = file + f"(1)"
    filename_out = file + '.' + ext
    return filename_out
