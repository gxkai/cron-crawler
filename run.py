from multiprocessing.sharedctypes import Value
import os
import pathlib2
import argparse
import importlib
from main import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Cron Job")
    parser.add_argument("--modules", nargs="+", required=True, help="path to modules to run")
    args = parser.parse_args()
    modules = args.modules
    for module_path in modules:
        run(pathlib2.Path(module_path))

