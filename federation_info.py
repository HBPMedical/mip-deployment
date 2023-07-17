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

# Experiment log is of format:
# 2022-10-26 06:32:59.145  INFO 12 --- [       Thread-7] eu.hbp.mip.utils.Logger                  :  User -> anonymous ,Endpoint -> (POST) /experiments ,Info ->  Finished the experiment: ExperimentDAO(uuid=760d9ded-f66e-49b6-ad34-dbae1dcad67b, name=One Way Anova, createdBy=UserDAO(username=anonymous, subjectId=anonymousId, fullname=anonymous, email=anonymous@anonymous.com, agreeNDA=true), workflowHistoryId=null, status=success, result=[{"anova_table":{"n_obs":825.0,"y_label":"leftententorhinalarea","x_label":"neurodegenerativescategories","df_residual":822.0,"df_explained":2.0,"ss_residual":37.01440328649596,"ss_explained":15.04582027432878,"ms_residual":0.045029687696467105,"ms_explained":7.52291013716439,"p_value":1.1102230246251565E-16,"f_stat":167.06556323184572},"tuckey_test":[{"groupA":"PD","groupB":"AD","meanA":1.7211585185185185,"meanB":1.4287119708029197,"diff":0.29244654771559886,"se":0.01659898611255717,"t_stat":17.61833799561784,"p_tuckey":0.001},{"groupA":"PD","groupB":"MCI","meanA":1.7211585185185185,"meanB":1.5088550684931508,"diff":0.21230345002536777,"se":0.020484309422929142,"t_stat":10.364198550317033,"p_tuckey":0.001},{"groupA":"AD","groupB":"MCI","meanA":1.4287119708029197,"meanB":1.5088550684931508,"diff":-0.08014309769023109,"se":0.02174314706679941,"t_stat":-3.6859014678976805,"p_tuckey":0.001}],"min_max_per_group":{"categories":["PD","AD","MCI"],"min":[1.0429,0.39954,0.39954],"max":[2.3952,1.9971,2.1113]},"ci_info":{"sample_stds":{"PD":0.1745754772473241,"AD":0.24280162815714373,"MCI":0.23944727425923165},"means":{"PD":1.7211585185185185,"AD":1.4287119708029197,"MCI":1.5088550684931508},"m-s":{"PD":1.5465830412711945,"AD":1.185910342645776,"MCI":1.269407794233919},"m+s":{"PD":1.8957339957658426,"AD":1.6715135989600634,"MCI":1.7483023427523825}}}], finished=2022-10-26 06:32:59.130, algorithm={"name":"anova_oneway","desc":null,"label":"One Way Anova","type":"exareme2","parameters":[{"name":"y","desc":null,"label":"y","type":null,"columnValuesSQLType":null,"columnValuesIsCategorical":null,"value":"leftententorhinalarea","defaultValue":null,"valueType":null,"valueNotBlank":null,"valueMultiple":null,"valueMin":null,"valueMax":null,"valueEnumerations":null},{"name":"x","desc":null,"label":"x","type":null,"columnValuesSQLType":null,"columnValuesIsCategorical":null,"value":"neurodegenerativescategories","defaultValue":null,"valueType":null,"valueNotBlank":null,"valueMultiple":null,"valueMin":null,"valueMax":null,"valueEnumerations":null},{"name":"pathology","desc":null,"label":"pathology","type":null,"columnValuesSQLType":null,"columnValuesIsCategorical":null,"value":"dementia:0.1","defaultValue":null,"valueType":null,"valueNotBlank":null,"valueMultiple":null,"valueMin":null,"valueMax":null,"valueEnumerations":null},{"name":"dataset","desc":null,"label":"dataset","type":null,"columnValuesSQLType":null,"columnValuesIsCategorical":null,"value":"desd-synthdata,ppmi","defaultValue":null,"valueType":null,"valueNotBlank":null,"valueMultiple":null,"valueMin":null,"valueMax":null,"valueEnumerations":null},{"name":"filter","desc":null,"label":"filter","type":null,"columnValuesSQLType":null,"columnValuesIsCategorical":null,"value":"{\"condition\": \"AND\", \"rules\": [{\"id\": \"dataset\", \"type\": \"string\", \"value\": [\"desd-synthdata\", \"ppmi\"], \"operator\": \"in\"}, {\"condition\": \"AND\", \"rules\": [{\"id\": \"neurodegenerativescategories\", \"type\": \"string\", \"operator\": \"is_not_null\", \"value\": null}, {\"id\": \"leftententorhinalarea\", \"type\": \"string\", \"operator\": \"is_not_null\", \"value\": null}]}], \"valid\": true}","defaultValue":null,"valueType":null,"valueNotBlank":null,"valueMultiple":null,"valueMin":null,"valueMax":null,"valueEnumerations":null}]}, algorithmId=anova_oneway, created=2022-10-26 06:32:52.589, updated=null, shared=false, viewed=false)

LOG_FILE_CHUNK_SIZE = 1024  # Will read the logfile in chunks
TIMESTAMP_REGEX = (
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}"  # 2022-04-13 18:25:22.875
)
EXPERIMENT_FINISHED_PATTERN = rf"({TIMESTAMP_REGEX})  INFO .*? User -> (.*?) ,Endpoint.*?Finished the experiment: .*?uuid=(.*?), name.*?, status=(.*?), result.*?, finished=(.*?), algorithm=(.*?), algorithmId.*? created=(.*?), updated.*?"
EXPERIMENT_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def print_audit_entry(log_line):
    if pattern_groups := re.search(EXPERIMENT_FINISHED_PATTERN, log_line):
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
            exp_finished_timedelta.seconds * 1000
            + exp_finished_timedelta.microseconds / 1000
        )
        
        algorithm_properties = json.loads(algorithm_properties_str)
        parameters = {
            par["name"]: par["value"] for par in algorithm_properties["parameters"]
        }
        print(
            f"{log_timestamp} - {user} - EXPERIMENT_FINISHED - {uuid} - {algorithm_properties['name']} - {parameters['pathology']} - {parameters['dataset']} - {status} - {exp_time_to_finish} - {parameters}"
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

