import subprocess


def exec(input: list[str]):
    command = " ".join(input)
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return {"code": process.returncode, "buffer": str(process.stdout)}
