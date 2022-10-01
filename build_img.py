import sys
import subprocess
import datetime
import argparse

options = None

versions = [
    # Trusty
    # "2.9", "3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8",
    # Xenial
    "3.9", "4", "5", "6",
    # Bionic
    "7", "8", "9", "10",
    # Focal
    "11", "12", "13", "14",
    # Jammy
    "15", "16"
    ]

test_versions = {"4": "4.0", "5": "5.0", "6": "6.0"}


def update_base_images():
    if not options.no_update_base:
        subprocess.check_call("docker pull ubuntu:xenial", shell=True)
        subprocess.check_call("docker pull ubuntu:bionic", shell=True)
        subprocess.check_call("docker pull ubuntu:focal", shell=True)


def run_my_cmd(cmd):
    try:
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    except Exception:
        print("Failure in command: " + cmd)
        raise

def build(version):
    tag = f"{options.repo}:{version}"

    force = "--no-cache"
    if options.no_force:
        force = ""

    cmd = f"docker build {force} --tag {tag} clang-{version}"
    run_my_cmd(cmd)
    return tag


def test(tag, test_version):
    cmd = f"docker run --rm {tag} clang++-{test_version} --version"
    expected = f"clang version {test_version}"
    try:
        print(cmd)
        output = subprocess.check_output(cmd, shell=True)
        if expected not in output.decode():
            msg = f"Expected output: \n{expected}\n"
            msg += f"Not found in actual output: \n{output}\n"
            raise AssertionError(msg)
        else:
            print("Corectly got:")
            print(output.decode())
    except Exception:
        print("Failure in command: " + cmd)
        raise


def tag_timestamp(base_tag, version):
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M")
    tag = f"{options.repo}:{version}_{timestamp}"
    cmd = f"docker tag {base_tag} {tag}"
    run_my_cmd(cmd)
    return tag


def tag_latest(base_tag):
    tag = f"{options.repo}:latest"
    cmd = f"docker tag {base_tag} {tag}"
    run_my_cmd(cmd)
    return tag


def push_tag(tag):
    cmd = f"docker push {tag}"
    run_my_cmd(cmd)

def create_and_push_manifest(time_tag):
    manifest_tag = f"{options.repo}:{options.version[0]}"
    cmd = f"docker manifest create {manifest_tag}"
    cmd += f" --amend {time_tag}"
    for additional in options.manifest_add:
        cmd += f" --amend {options.repo}:{additional}"
    run_my_cmd(cmd)

    cmd = f"docker manifest push {manifest_tag}"
    run_my_cmd(cmd)

def remove_tag(tag):
    cmd = f"docker rmi {tag}"
    run_my_cmd(cmd)


def all():
    for version in versions:
        build_one(version)


def build_one(version):
    tags = []
    base_tag = None
    time_tag = None
    latest_tag = None

    if not options.no_build:
        base_tag = build(version)

    if not options.no_test:
        tv = version
        if version in test_versions:
            tv = test_versions[version]

        test(base_tag, tv)

    if not options.no_tag_timestamp:
        time_tag = tag_timestamp(base_tag, version)

    if not options.no_latest:
        latest_tag = tag_latest(base_tag)

    if options.no_push_tag or options.manifest_add:
        base_tag = None

    if options.push:
        for tag in (base_tag, time_tag, latest_tag):
            if tag:
                push_tag(tag)

    if options.manifest_add:
        create_and_push_manifest(time_tag)

    if options.delete_timestamp_tag:
        remove_tag(time_tag)


def set_options():
    parser = argparse.ArgumentParser(
        description="Build one or more docker images for clang-ubuntu")
    parser.add_argument(
        "-v", "--version", action="append",
        help="Use one of more times to specify the versions to run, skip"
        + " for all")
    parser.add_argument(
        "--no-update-base", action="store_true",
        help="Don't update the base images")
    parser.add_argument(
        "--no-build", action="store_true", help="skip build step")
    parser.add_argument(
        "--no-force", action="store_true",
        help="don't force an update, use existing layers")
    parser.add_argument(
        "--no-test", action="store_true", help="skip the test step")
    parser.add_argument(
        "--no-tag-timestamp", action="store_true", help="only version tag")
    parser.add_argument(
        "--no-latest", action="store_true",
        help="don't update each to latest tag, whichever version is"
        + " specified last will win")
    parser.add_argument(
        "-T", "--no-push-tag", action="store_true",
        help="Do not apply the tag for the version, only the timestamp tag")
    parser.add_argument(
        "-r", "--repo", default="test/clang",
        help="repo to build for and push to. Default is test/clang, "+
        "use teeks99/clang-ubuntu for dockerhub")
    parser.add_argument(
        "-p", "--push", action="store_true", help="push to dockerhub")
    parser.add_argument(
        "-d", "--delete-timestamp-tag", action="store_true",
        help="remove the timestamp tag from the local machine")
    parser.add_argument(
        "-m", "--manifest-add", action="append",
        help="Generate a manifest for the version supplied, using the" +
        " timestamp upload as the first version add the timestamp(s)" +
        " specified here as additional versions. Used for generating" + 
        " multiarch images on different machines.")

    global options
    options = parser.parse_args()

    if options.manifest_add and len(options.version) > 1:
        raise RuntimeError("Cannot support manifest with multiple versions")


def run():
    set_options()

    if options.version:
        global versions
        versions = options.version

    update_base_images()

    all()


if __name__ == "__main__":
    run()
