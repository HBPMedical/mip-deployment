import subprocess
import re


EXPERIMENTS_EXECUTED = 18
EXPERIMENT_AUDIT_ENTRY_IDENTIFIER = " - EXPERIMENT_FINISHED - "
SPECIFIC_EXPERIMENT_PATTERN = ".*? - anonymous - EXPERIMENT_FINISHED - .*? - NAIVE_BAYES - dementia:0.1 - edsd - success - .*? - .*?\\n.*"


def test_federation_info():
    cmd = f"docker logs backend_components_portalbackend_1 | python3 ../../federation_info.py show-portal-backend-audit-entries"
    res = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert res.returncode == 0

    str_output = res.stdout.decode()

    assert (
        len(str_output.split(EXPERIMENT_AUDIT_ENTRY_IDENTIFIER)) == EXPERIMENTS_EXECUTED
    )

    assert re.match(SPECIFIC_EXPERIMENT_PATTERN, str_output)

