import subprocess


def exec(command: str, input: list[str]):
    arguments = " ".join(input)
    fullcommand = f"{command} {arguments}"
    process = subprocess.run(fullcommand, shell=True, capture_output=True)
    return {"code": process.returncode, "buffer": str(process.stdout)}
