import json
import re
from datetime import datetime
from sys import stdin

import click

LOG_FILE_CHUNK_SIZE = 1024  # Will read the logfile in chunks
TIMESTAMP_REGEX = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}"  # 2022-04-13 18:25:22.875
EXPERIMENT_FINISHED_PATTERN = (
    rf"({TIMESTAMP_REGEX}) - INFO .*? User -> (.*?) , Endpoint.*?Experiment finished: .*?uuid=(.*?), name.*?, status=(.*?), "
    rf"result.*?, finished=(.*?), algorithm=(.*?), algorithmId.*? created=(.*?), updated.*?"
)
USER_LOGGING_IN_PATTERN = (
    rf"({TIMESTAMP_REGEX}) - INFO .*? User -> (.*?) , Endpoint -> LOGGING IN , Info ->  User (.*?) has logged in successfully"
)
USER_AUTHORITY_PATTERN = (
    rf"({TIMESTAMP_REGEX}) - INFO .*? User -> (.*?) , Endpoint -> LOGGING IN , Info ->  User (.*?) has authority (.*?)"
)
TRANSIENT_EXPERIMENT_PATTERN = (
    rf"({TIMESTAMP_REGEX}) - INFO .*? User -> (.*?) , Endpoint -> \(POST\) /experiments/transient , Info ->  Request for transient experiment creation\. RequestBody: (.*)"
)
EXPERIMENT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


@click.group()
def cli():
    """
    This is a log aggregation script.
    It can be used either in a local hospital node to show database actions or in the federation master node
    to show information for all the federation nodes.
    """
    pass


def parse_experiment_finished_log(pattern_groups):
    log_timestamp = pattern_groups[1]
    user = pattern_groups[2]
    uuid = pattern_groups[3]
    status = pattern_groups[4]
    algorithm_properties_str = pattern_groups[6]
    exp_created = pattern_groups[7]
    exp_finished = pattern_groups[5]

    # Calculate experiment time to finish.
    exp_created_dt = datetime.strptime(exp_created, EXPERIMENT_TIMESTAMP_FORMAT)
    exp_finished_dt = datetime.strptime(exp_finished, EXPERIMENT_TIMESTAMP_FORMAT)
    exp_finished_timedelta = exp_finished_dt - exp_created_dt
    exp_time_to_finish = int(
        exp_finished_timedelta.total_seconds() * 1000
    )

    algorithm_properties = json.loads(algorithm_properties_str)
    parameters = {par["name"]: par["value"] for par in algorithm_properties["parameters"]}

    print(
        f"{log_timestamp} - {user} - EXPERIMENT_FINISHED - {uuid} - {algorithm_properties['name']} - {parameters.get('pathology', 'N/A')} - {parameters.get('dataset', 'N/A')} - {status} - {exp_time_to_finish}ms - {parameters} - {algorithm_properties.get('preprocessing', 'N/A')}"
    )


def parse_transient_experiment_log(pattern_groups):
    log_timestamp = pattern_groups[1]
    user = pattern_groups[2]
    request_body_str = pattern_groups[3]
    request_body = json.loads(request_body_str)
    name = request_body["name"]
    algorithm = request_body["algorithm"]["name"]
    parameters = {par["name"]: par["value"] for par in request_body["algorithm"]["parameters"]}

    print(
        f"{log_timestamp} - {user} - TRANSIENT_EXPERIMENT - {name} - {algorithm} - {parameters.get('pathology', 'N/A')} - {parameters.get('dataset', 'N/A')} - {parameters} - {request_body['algorithm'].get('preprocessing', 'N/A')}"
    )


def parse_user_logged_in_log(pattern_groups):
    log_timestamp = pattern_groups[1]
    user = pattern_groups[2]
    print(f"{log_timestamp} - {user} - USER LOGGED IN")


def parse_user_authority_log(pattern_groups):
    log_timestamp = pattern_groups[1]
    user = pattern_groups[2]
    authority = pattern_groups[4]
    print(f"{log_timestamp} - {user} - USER AUTHORITY - {authority}")


def print_audit_entry(log_line):
    if pattern_groups := re.search(EXPERIMENT_FINISHED_PATTERN, log_line):
        parse_experiment_finished_log(pattern_groups)
    elif pattern_groups := re.search(USER_LOGGING_IN_PATTERN, log_line):
        parse_user_logged_in_log(pattern_groups)
    elif pattern_groups := re.search(USER_AUTHORITY_PATTERN, log_line):
        parse_user_authority_log(pattern_groups)
    elif pattern_groups := re.search(TRANSIENT_EXPERIMENT_PATTERN, log_line):
        parse_transient_experiment_log(pattern_groups)


@cli.command()
@click.option(
    "--logfile",
    help="The logfile to get the audit entries from. Will use stdin if not provided.",
    type=click.File("r"),
    default=stdin,
)
def show_portal_backend_audit_entries(logfile):
    previous_chunk_remains = ""
    while logs_chunk := logfile.read(LOG_FILE_CHUNK_SIZE):
        logs_chunk = previous_chunk_remains + logs_chunk
        # Separate lines when "\n2022-04-13 18:25:22.875 - is found
        separate_log_lines = re.split(rf"\n(?={TIMESTAMP_REGEX})", logs_chunk)

        # The final log_line could be incomplete due to "chunking"
        for log_line in separate_log_lines[:-1]:
            print_audit_entry(log_line)
        previous_chunk_remains = separate_log_lines[-1]
    else:
        print_audit_entry(previous_chunk_remains)


if __name__ == "__main__":
    cli()
