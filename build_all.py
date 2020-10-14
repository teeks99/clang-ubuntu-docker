import sys
import subprocess

repo = 'test/clang'

versions = [
    "2.9", "3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9",
    "4", "5", "6", "7", "8", "9", "10", "11", "12",
    ]

if len(sys.argv) == 2:
    repo = sys.argv[1]

for version in versions:
    cmd = f"docker build clang-{version} -t {repo}:{version}"
    print(cmd)
    subprocess.check_call(cmd, shell=True)