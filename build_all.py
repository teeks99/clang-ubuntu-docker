import sys
import subprocess
import datetime

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

subprocess.check_call("docker pull ubuntu:xenial", shell=True)
subprocess.check_call("docker pull ubuntu:bionic", shell=True)
subprocess.check_call("docker pull ubuntu:focal", shell=True)

test_versions = {"4": "4.0", "5": "5.0", "6": "6.0"}

if len(sys.argv) == 2:
    repo = sys.argv[1]


def build(version):
    cmd = f"docker build --no-cache --tag {repo}:{version} clang-{version}"
    print(cmd)
    try:
        subprocess.check_call(cmd, shell=True)
    except:
        print("Failure in command: " + cmd)
        raise


def test(version):
    tv = version
    if version in test_versions:
        tv = test_versions[version]

    cmd = f"docker run --rm {repo}:{version} clang++-{tv} --version"
    expected = f"clang version {tv}"
    print(cmd)
    try:
        output = subprocess.check_output(cmd, shell=True)
        if not expected in output.decode():
            msg += f"Expected output: \n{expected}\n"
            msg += f"Not found in actual output: \n{output}\n"
            raise AssertionError(msg)
    except:
        print("Failure in command: " + cmd)
        raise


def tag(version):
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M")
    cmd = f"docker tag {repo}:{version} {repo}:{version}_{timestamp}"
    try:
        subprocess.check_call(cmd, shell=True)
    except:
        print("Failure in command: " + cmd)
        raise


for version in versions:
    build(version)
    test(version)
    tag(version)
