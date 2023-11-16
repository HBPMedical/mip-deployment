import subprocess


EXPERIMENTS_EXECUTED = 17
EXPERIMENT_AUDIT_ENTRY_IDENTIFIER = " - EXPERIMENT_FINISHED - "


def test_federation_info():
    cmd = f"docker logs dev_portalbackend_1 | python3 ../federation_info.py show-portal-backend-audit-entries"
    res = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert res.returncode == 0

    str_output = res.stdout.decode()

    assert (
        len(str_output.split(EXPERIMENT_AUDIT_ENTRY_IDENTIFIER)) == EXPERIMENTS_EXECUTED
    )
