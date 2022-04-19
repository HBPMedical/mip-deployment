import json
import re
from contextlib import contextmanager
from sys import stdin
from datetime import datetime

import click


@click.group()
def cli():
    """
    This is a log aggregation script.
    It can be used either in a local hospital node to show database actions or in the federation master node
    to show information for all the federation nodes.
    """
    pass


LOG_FILE_CHUNK_SIZE = 1024  # Will read the logfile in chunks
TIMESTAMP_REGEX = (
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}"  # 2022-04-13 18:25:22.875
)
# Experiment log is of format:
# 2022-04-18 14:07:21.042 - anonymous - EXPERIMENT_FINISHED - Pearson Correlation - pathology - datasets - error - 1s - [{"name":"y","desc":null,"label":null,"type":null,"columnValuesSQLType":null,"columnValuesIsCategorical":null,"value":"rightsplsuperiorparietallobule,rightttgtransversetemporalgyrus,leftcaudate,leftocpoccipitalpole","defaultValue":null,"valueType":null,"valueNotBlank":null,"valueMultiple":null,"valueMin":null,"valueMax":null,"valueEnumerations":null},{"name":"pathology","desc":null,"label":null,"type":null,"columnValuesSQLType":null,"columnValuesIsCategorical":null,"value":"dementia:0.1","defaultValue":null,"valueType":null,"valueNotBlank":null,"valueMultiple":null,"valueMin":null,"valueMax":null,"valueEnumerations":null},{"name":"dataset","desc":null,"label":null,"type":null,"columnValuesSQLType":null,"columnValuesIsCategorical":null,"value":"edsd0,edsd1,edsd8,edsd9","defaultValue":null,"valueType":null,"valueNotBlank":null,"valueMultiple":null,"valueMin":null,"valueMax":null,"valueEnumerations":null},{"name":"filter","desc":null,"label":null,"type":null,"columnValuesSQLType":null,"columnValuesIsCategorical":null,"value":"","defaultValue":null,"valueType":null,"valueNotBlank":null,"valueMultiple":null,"valueMin":null,"valueMax":null,"valueEnumerations":null},{"name":"alpha","desc":null,"label":null,"type":null,"columnValuesSQLType":null,"columnValuesIsCategorical":null,"value":"0.9529895484370635","defaultValue":null,"valueType":null,"valueNotBlank":null,"valueMultiple":null,"valueMin":null,"valueMax":null,"valueEnumerations":null}]
EXPERIMENT_FINISHED_PATTERN = rf"({TIMESTAMP_REGEX})  INFO .* User -> (.*) ,Endpoint.*Finished the experiment: .*uuid=(.*), name.*, status=(.*), result.*, finished=(.*), algorithm=.*\"label\":\"(.*)\",.*\"parameters\":(.*)\}}, algorithmId.* created=(.*), updated.*"
EXPERIMENT_PARAMETER_PATTERN = '.*"name":"(.*)","desc".*,"value":"(.*)","defaultValue".*'
EXPERIMENT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def print_audit_entry(log_line):
    if pattern_groups := re.search(EXPERIMENT_FINISHED_PATTERN, log_line):
        log_timestamp = pattern_groups[1]
        user = pattern_groups[2]
        uuid = pattern_groups[3]
        status = pattern_groups[4]
        algorithm = pattern_groups[6]
        parameters_str = pattern_groups[7]
        exp_created = pattern_groups[8]
        exp_finished = pattern_groups[5]

        # Split parameters and then parse each one to get the name/value
        parameters = {}
        for parameter_str in parameters_str.split("},"):
            parameter_ptr_groups = re.search(
                EXPERIMENT_PARAMETER_PATTERN, parameter_str
            )
            parameters[parameter_ptr_groups[1]] = parameter_ptr_groups[2]

        # The time an experiment took is the finished-created time.
        exp_created_dt = datetime.strptime(exp_created, EXPERIMENT_TIMESTAMP_FORMAT)
        exp_finished_dt = datetime.strptime(exp_finished, EXPERIMENT_TIMESTAMP_FORMAT)
        exp_finished_timedelta = exp_finished_dt - exp_created_dt
        exp_time_to_finish = int(exp_finished_timedelta.seconds*1000 + exp_finished_timedelta.microseconds/1000)
        print(
            f"{log_timestamp} - {user} - EXPERIMENT_FINISHED - {uuid} - {algorithm} - {parameters['pathology']} - {parameters['dataset']} - {status} - {exp_time_to_finish} - {parameters}"
        )


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
