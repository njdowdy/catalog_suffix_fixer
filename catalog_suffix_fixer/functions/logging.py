from loguru import logger
import sys


def log_start(log_location: str = "catalog_suffix_fixer/logs/") -> None:
    """
    Log when the script was run and who initiated it
    """
    logger.add(f"{log_location}log_" + "{time}.log", enqueue=True, rotation="10 MB")
    logger.add(
        sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO"
    )
    logger.info("admin: Logging started...")


def log_watchdog_startup(to_watch: str = "."):
    logger.info(
        "admin: Veranus worker began monitoring {to_watch}...", to_watch=to_watch
    )


def log_job_summary(
    job_id: str = "NA",
    user: str = "anonymous",
    department: str = "???",
    file_in: str = "file_in",
    file_out: str = "file_out",
    processed: int = 0,
    generated: int = 0,
    total: int = 0,
) -> None:
    """ """
    logger.info(
        "JOB ID: {job_id} -- Submitter: {user} | Dept.: {department} | [{file_in}] >> [{file_out}] | Processed {processed} | Generated {generated} | New Total: {total} | JOB COMPLETE!",
        job_id=job_id,
        user=user,
        department=department,
        file_in=file_in,
        file_out=file_out,
        processed=processed,
        generated=generated,
        total=total,
    )


def log_processing_event(job_id: str = "NA", file_in: str = "file_in", statement: str = "") -> None:
    logger.info("JOB ID: {job_id} -- {file_in}{statement}", job_id=job_id, file_in=file_in, statement=statement)
