from json import load, dump, JSONDecodeError
from datetime import datetime
import os

def write_build_to_json():
    """
    Write a build to builds.json
    """
    FILE_NAME = "builds.json"
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            dump({}, f)

    with open(FILE_NAME, "r") as f:
        try:
            data = load(f)
        except JSONDecodeError:
            data = {}

    # get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data[len(data)] = current_time

    with open(FILE_NAME, "w") as f:
        dump(data, f)
