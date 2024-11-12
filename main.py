import logging
import pathlib2
import importlib
from src import constant
from src.util import loadenv
import sys

logger = logging.Logger(name="Cron Job", level=logging.INFO)
std_handler = logging.StreamHandler(sys.stdout)
std_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
std_handler.setFormatter(formatter)
logger.addHandler(std_handler)

loadenv()

def run(path: pathlib2.Path):
    path = path.absolute()
    name = path.name
    if name == "__pycache__":
        return
    if path.is_file():
        module = name.split('.')[0]
        rel_path = path.relative_to(constant.JOBS_PATH)
        prefix = ".".join(str(rel_path).split("/")[:-1])
        module_path = f"jobs.{prefix}.{module}" if len(prefix) != 0 else f"jobs.{module}"
        logger.info(f"Load and run job {module_path}")
        try:
            job = importlib.import_module(module_path)
            if hasattr(job, "Job"):
                # current file has no Job class, could be a helper file, skip
                j = job.Job()
                j.run()
        except ModuleNotFoundError as e:
            logger.warning(e)
    else:
        for path in path.iterdir():
            run(path)


if __name__ == "__main__":
    run(constant.JOBS_PATH)
