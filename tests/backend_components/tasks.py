import json
import os
import pathlib
from enum import Enum
from itertools import cycle
from textwrap import indent
from time import sleep

from invoke import UnexpectedExit
from invoke import task


wheel = cycle(r"-\|/")

this_mod_path = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_FOLDER = pathlib.Path(this_mod_path).parent.parent / "data"


def spin_wheel(promise=None, time=None):
    dt = 0.15
    if promise is not None:
        print("  ", end="")
        for frame in wheel:
            print(frame + "  ", sep="", end="", flush=True)
            sleep(dt)
            print("\b\b\b", sep="", end="", flush=True)
            if promise.runner.process_is_finished:
                print("\b\b", end="")
                break
    elif time:
        print("  ", end="")
        for frame in wheel:
            print(frame + "  ", sep="", end="", flush=True)
            sleep(dt)
            print("\b\b\b", sep="", end="", flush=True)
            time -= dt
            if time <= 0:
                print("\b\b", end="")
                break


def run(c, cmd, attach_=False, wait=True, warn=False, raise_error=False, show_ok=True):
    if attach_:
        c.run(cmd, pty=True)
        return

    if not wait:
        c.run(cmd, disown=True)
        # nevertheless, it will wait (sleep) for 4 seconds here, why??
        spin_wheel(time=4)
        if show_ok:
            message("Ok", Level.SUCCESS)
        return

    promise = c.run(cmd, asynchronous=True, warn=warn)
    spin_wheel(promise=promise)
    stderr = promise.runner.stderr
    if stderr and raise_error:
        raise UnexpectedExit(stderr)
    result = promise.join()
    if show_ok:
        message("Ok", Level.SUCCESS)
    return result


class Level(Enum):
    HEADER = ("cyan", 1)
    BODY = ("white", 2)
    SUCCESS = ("green", 1)
    ERROR = ("red", 1)
    WARNING = ("yellow", 1)


def message(msg, level=Level.BODY):
    if msg.endswith("..."):
        end = ""
    else:
        end = "\n"
    color, indent_level = level.value
    prfx = "  " * indent_level
    print(indent(msg, prfx), end=end, flush=True)


@task
def setup_dbs(c):
    """Install project dependencies using poetry."""
    message("Installing dependencies...", Level.HEADER)
    cmd = "poetry install"
    run(c, cmd)
    datasets_per_data_model = {}

    datasets_per_location = {
        50001: {
            "longitudinal_dementia": ["longitudinal_dementia"],
            "dementia": ["desd-synthdata.csv", "ppmi.csv"],
            "tbi": ["dummy_tbi.csv"],
        },
        50002: {
            "dementia": ["edsd.csv", "fake_longitudinal.csv"],
            "mentalhealth": ["demo.csv"],
        },
    }

    for port in datasets_per_location.keys():
        message(f"Initializing MonetDB with mipdb in port: {port}...", Level.HEADER)
        cmd = f"""poetry run mipdb init --ip 127.0.0.1 --port {port}  --username admin --password admin --db_name db"""
        run(c, cmd)

        data_model_folders = [
            TEST_DATA_FOLDER / folder for folder in os.listdir(TEST_DATA_FOLDER)
        ]
        for data_model_folder in data_model_folders:
            with open(
                data_model_folder / "CDEsMetadata.json"
            ) as data_model_metadata_file:
                data_model_metadata = json.load(data_model_metadata_file)
                data_model_code = data_model_metadata["code"]
                data_model_version = data_model_metadata["version"]
                data_model = f"{data_model_code}:{data_model_version}"
            cdes_file = data_model_folder / "CDEsMetadata.json"

            if data_model_code not in datasets_per_location[port].keys():
                continue

            message(
                f"Loading data model '{data_model_code}:{data_model_version}' metadata to database (127.0.0.1:{port})",
                Level.HEADER,
            )
            cmd = f"mipdb add-data-model {cdes_file} --ip 127.0.0.1 --port {port} --username admin --password admin --db_name db"
            run(c, cmd)

            csvs = sorted(
                [
                    data_model_folder / file
                    for file in os.listdir(data_model_folder)
                    if file in datasets_per_location[port][data_model_code]
                ]
            )

            for csv in csvs:
                cmd = f"mipdb add-dataset {csv} -d {data_model_code} -v {data_model_version} --copy_from_file false --ip 127.0.0.1 --port {port} --username admin --password admin --db_name db"
                run(c, cmd)

                message(
                    f"Loading dataset {pathlib.PurePath(csv).name} to database (127.0.0.1:{port})",
                    Level.HEADER,
                )
                datasets_per_data_model[data_model] = pathlib.PurePath(csv).name
        message(f"Data loaded to database (127.0.0.1:{port})", Level.HEADER)
