import subprocess


def exec(command: str, input: list[str]):
    buffer = ""
    arguments = " ".join(input)
    proc = subprocess.Popen(
        f"{command} {arguments}",
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()
    buffer = stdout.decode("utf-8") + stderr.decode("utf-8")
    code = proc.returncode
    return {"buffer": buffer, "code": code}
