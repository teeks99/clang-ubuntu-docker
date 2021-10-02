import sys
import subprocess

repo = 'test/clang'

versions = [
    # Trusty
    #"2.9", "3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", 
    # Xenial
    "3.9", "4", "5", "6", 
    # Bionic
    "7", "8", "9", "10", 
    # Focal
    "11", "12", "13", "14"
    ]

if len(sys.argv) == 2:
    repo = sys.argv[1]

for version in versions:
    cmd = f"docker build clang-{version} -t {repo}:{version}"
    print(cmd)
    try:
        subprocess.check_call(cmd, shell=True)
    except:
        print("Failure in command: " + cmd)
        raise