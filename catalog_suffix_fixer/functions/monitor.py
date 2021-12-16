import time
import os
import re
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from catalog_suffix_fixer.functions import parsing as parse
from catalog_suffix_fixer.functions import logging as log


def start_monitor(to_watch: str = "catalog_suffix_fixer/input/") -> None:
    # setup and define event handler
    event_handler = PatternMatchingEventHandler(
        patterns=["*.csv"],
        ignore_patterns=[],
        ignore_directories=True,
        case_sensitive=True,
    )
    event_handler.on_created = on_created
    event_handler.on_modified = on_modified
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


def queue_existing(mypath: str) -> None:
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.utime(os.path.join(root, file))


def file_process(file: str) -> None:
    filestub = "/".join(file.split("/")[2:])
    file_exists = os.path.exists(file)
    if file_exists:
        log.log_processing_event(filestub, " was detected...")
        time.sleep(0.1)
        # check if file exists in staging
        file_stage = f"{file.replace('input', 'staging')}"
        file_stage = resolve_destination_path(
            path=file_stage, stub=filestub, classification="staging"
        )
        # move to output
        move_file(
            path_in=file, path_out=file_stage, stub=filestub, classification="staging"
        )
        # do a thing
        df = parse.import_data(file_stage)
        df = parse.sort_df(df)
        df = parse.remove_empty_rows(df)
        processed_count = parse.number_processed(df)
        df = parse.generate_new_records(df)
        generated_count = parse.number_generated(df, processed_count)
        new_total_count = processed_count + generated_count
        # check if file exists in output
        file_out = f"{file_stage.replace('staging', 'output')}"
        file_out = resolve_destination_path(
            path=file_out, stub=filestub, classification="processing"
        )
        parse.save_df(df, file_out)
        # check if file exists in processed
        file_proc = f"{file_stage.replace('staging', 'processed')}"
        file_proc = resolve_destination_path(path=file_proc, stub=filestub)
        # move to output
        move_file(path_in=file_stage, path_out=file_proc, stub=filestub)
        log.log_job_summary(
            user=file.split("/")[-1].split("_")[0],
            department=file.split("/")[-2],
            file_in=file,
            file_out=file_out,
            processed=processed_count,
            generated=generated_count,
            total=new_total_count,
        )


def move_file(
    path_in: str, path_out: str, stub: str, classification: str = "moving"
) -> None:
    os.makedirs("/".join(path_out.split("/")[0:-1]), exist_ok=True)
    if classification == "staging":
        statement = " was staged for processing..."
    elif classification == "moving":
        statement = " was processed and moved..."
    else:
        statement = "!"
    os.rename(path_in, path_out)
    log.log_processing_event(stub, statement)


def resolve_destination_path(
    path: str, stub: str, classification: str = "moving"
) -> str:
    if os.path.exists(path):
        while os.path.exists(path):
            path = rename_duplicate_file(path)  # if it does, rename it
        file_out_stub = "/".join(path.split("/")[2:])
        if classification == "staging":
            statement = f" exists in staging area. Renamed to: {file_out_stub}"
        elif classification == "moving":
            statement = f" exists in output directory. Renamed to: {file_out_stub}"
        elif classification == "processing":
            statement = f" exists in processed directory. Renamed to: {file_out_stub}"
        else:
            statement = "renamed!"
        log.log_processing_event(stub, statement)
        return path
    else:
        return path


def on_modified(event) -> None:
    file_process(event.src_path)


def on_created(event) -> None:
    file_process(event.src_path)


def rename_duplicate_file(filename: str) -> str:
    file = ".".join(filename.split(".")[0:-1])
    ext = filename.split(".")[-1]
    suffix = re.search(r"\(([0-9]+)\)", file)
    if suffix:
        suffix_value = int(suffix.group(1))
        file = re.sub(rf"\({suffix_value}\)", f"({suffix_value + 1})", file)
    else:
        file = file + f"(1)"
    filename_out = file + "." + ext
    return filename_out
