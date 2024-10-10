from json import load, dump, JSONDecodeError
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BUILDS_FILE_NAME = os.environ.get("BUILDS_FILE_NAME", "builds.json")

def write_build_to_json():
    """
    Write a build to builds.json
    """
    if not os.path.exists(BUILDS_FILE_NAME):
        with open(BUILDS_FILE_NAME, "w") as f:
            dump({}, f)

    with open(BUILDS_FILE_NAME, "r") as f:
        try:
            data = load(f)
        except JSONDecodeError:
            data = {}

    # get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data[len(data)] = current_time

    with open(BUILDS_FILE_NAME, "w") as f:
        dump(data, f)
