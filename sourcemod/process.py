import subprocess


def exec(input: list[str]):
    process = subprocess.run(
        " ".join(input), shell=True, capture_output=True, text=True
    )
    return {"code": process.returncode, "buffer": str(process.stdout)}
