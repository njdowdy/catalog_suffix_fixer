import time
import os
import re
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def start_monitor(to_watch: str = 'catalog_suffix_fixer/input/'):
    # setup and define event handler
    event_handler = PatternMatchingEventHandler(patterns=["*.txt", "*.csv"], ignore_patterns=[],
                                                ignore_directories=True, case_sensitive=True)
    event_handler.on_created = on_created
    event_handler.on_modified = on_modified
    print(f"Veranus began monitoring: {to_watch}")
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


def queue_existing(mypath: str):
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.utime(os.path.join(root, file))


def file_process(file: str):
    filestub = '/'.join(file.split('/')[2:])
    print(f"{filestub} has been detected.")
    # do a thing
    # time.sleep(2)
    # check if file exists in output
    file_out = f"{file.replace('input', 'output')}"
    file_out = check_file_exists(path=file_out, stub=filestub)
    # move to output
    move_file(path_in=file, path_out=file_out, stub=filestub)


def move_file(path_in: str, path_out: str, stub: str):
    os.makedirs('/'.join(path_out.split('/')[0:-1]), exist_ok=True)
    os.rename(path_in, path_out)
    print(f"{stub} has been processed and moved!")


def check_file_exists(path: str, stub: str):
    if os.path.exists(path):
        while os.path.exists(path):
            path = rename_duplicate_file(path)  # if it does, rename it
        file_out_stub = '/'.join(path.split('/')[2:])
        print(f"{stub} exists in output directory. Renamed to: {file_out_stub}")
        return path
    else:
        return path


def on_modified(event):
    file_process(event.src_path)


def on_created(event):
    file_process(event.src_path)


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
