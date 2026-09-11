import sys
import subprocess
import datetime
import argparse
import json
import platform

options = None
push_log = {"versions":{}}

class Image(object):
    def __init__(self, repo, tag):
        self.repo = repo
        self.tag = tag

    @property
    def image(self):
        return f"{self.repo}:{self.tag}"


def run_my_cmd(cmd):
    try:
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    except Exception:
        print("Failure in command: " + cmd)
        raise

def build(version):
    image = Image(options.repo, version)

    force = "--no-cache"
    if options.no_force:
        force = ""

    pull = "--pull"
    if options.no_update_base:
        pull = ""

    cmd = f"docker build {pull} {force} --tag {image.image} clang-{version}"
    run_my_cmd(cmd)
    return image


SMOKE_PASSED = "SMOKE TEST PASSED"

# Compiled and run inside the image by the smoke test. Reports the clang version
# it was built with and which standard library it picked up, so the test can
# tell a libc++ build from a libstdc++ one.
HELLO_WORLD = """\
#include <iostream>
#include <string>
#include <vector>

int main()
{
    std::vector<std::string> words = {"hello", "world"};
    std::string message;
    for (const std::string& word : words)
    {
        if (!message.empty())
        {
            message += ", ";
        }
        message += word;
    }

    std::cout << message << std::endl;
    std::cout << "clang major: " << __clang_major__ << std::endl;
#ifdef _LIBCPP_VERSION
    std::cout << "stdlib: libc++ " << _LIBCPP_VERSION << std::endl;
#else
    std::cout << "stdlib: libstdc++" << std::endl;
#endif
    return 0;
}
"""

# Fed to bash on the container's stdin, with the clang version as $1. Checks the
# versioned compiler and both unversioned symlinks, then actually builds and
# runs hello world, once with the default standard library and once with libc++.
SMOKE_TEST = """\
set -eu

version="$1"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

fail() {
    echo "SMOKE TEST FAILED: $*" >&2
    exit 1
}

contains() {
    case "$1" in
        *"$2"*) return 0 ;;
        *) return 1 ;;
    esac
}

check_version() {
    compiler="$1"
    echo "--- $compiler --version"
    output="$("$compiler" --version 2>&1)" || fail "could not run $compiler --version"
    echo "$output"
    contains "$output" "clang version $version" \\
        || fail "$compiler is not clang version $version"
}

build_and_run() {
    label="$1"
    expect="$2"
    shift 2
    echo "--- clang++ $* -o hello_$label hello.cpp"
    clang++ "$@" -o "$work/hello_$label" "$work/hello.cpp" \\
        || fail "clang++ $* could not compile hello world"
    output="$("$work/hello_$label" 2>&1)" || fail "the $label hello world would not run"
    echo "$output"
    contains "$output" "hello, world" \\
        || fail "the $label hello world printed the wrong thing"
    contains "$output" "clang major: $version" \\
        || fail "the $label hello world was not built by clang $version"
    if [ -n "$expect" ]; then
        contains "$output" "$expect" \\
            || fail "the $label hello world did not use $label"
    fi
}

cat > "$work/hello.cpp" <<'END_OF_HELLO_WORLD'
""" + HELLO_WORLD + ("""END_OF_HELLO_WORLD

# The versioned binary, plus the unversioned symlinks the Dockerfile makes.
check_version "clang++-$version"
check_version clang++
check_version clang

# The default standard library is libstdc++ on these images, but only libc++ is
# asserted: a default that moves is upstream's business, a libc++ that doesn't
# work is ours.
build_and_run default "" -std=c++17
build_and_run libc++ "stdlib: libc++" -std=c++17 -stdlib=libc++

echo "%s"
""" % SMOKE_PASSED)


def test(image, test_version):
    cmd = f"docker run --rm -i {image.image} bash -s {test_version}"
    print(cmd)
    result = subprocess.run(
        cmd, shell=True, input=SMOKE_TEST.encode(),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.decode()
    print(output)
    if result.returncode != 0 or SMOKE_PASSED not in output:
        raise AssertionError(f"Smoke test failed for {image.image}")


def tag_timestamp(base_image, version):
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M")
    arch_str = f"_{options.arch}" if options.arch else ""
    tag = f"{version}{arch_str}_{timestamp}"
    image = Image(options.repo, tag)
    cmd = f"docker tag {base_image.image} {image.image}"
    run_my_cmd(cmd)
    return image


def tag_latest(base_image):
    image = Image(options.repo,"latest")
    cmd = f"docker tag {base_image.image} {image.image}"
    run_my_cmd(cmd)
    return image


def push_image(image):
    cmd = f"docker push {image.image}"
    run_my_cmd(cmd)


def create_and_push_manifest(version_tag, amend_tags):
    manifest_image = Image(options.repo, version_tag)
    cmd = f"docker manifest rm {manifest_image.image}"
    try:
        run_my_cmd(cmd)
    except subprocess.CalledProcessError:
        pass

    cmd = f"docker manifest create {manifest_image.image}"
    for tag in amend_tags:
        cmd += f" --amend {options.repo}:{tag}"
    run_my_cmd(cmd)

    cmd = f"docker manifest push {manifest_image.image}"
    run_my_cmd(cmd)


def remove_image(image):
    cmd = f"docker rmi {image.image}"
    run_my_cmd(cmd)


def build_one(version, push_latest=False):
    tags = []
    base_image = None
    time_image = None
    latest_image = None

    if options.manifest_only:
        amend_tags = options.manifest_only
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M")
        time_tag = f"{version}_{timestamp}"

        create_and_push_manifest(time_tag, amend_tags)
        create_and_push_manifest(version, amend_tags)
        if push_latest:
            create_and_push_manifest("latest", amend_tags)

        pushes = {}
        pushes["timestamp"] = time_tag
        if push_latest:
            pushes["latest"] = True
        push_log["versions"][version] = pushes
        return

    if not options.no_build:
        base_image = build(version)

    if not options.no_test:
        test(base_image, version)

    if not options.no_tag_timestamp:
        time_image = tag_timestamp(base_image, version)

    if push_latest:
        if not options.manifest_add:
            latest_image = tag_latest(base_image)

    if options.no_push_tag or options.manifest_add:
        base_image = None

    if options.push:
        for img in (base_image, time_image, latest_image):
            if img:
                push_image(img)

        pushes = {}
        if base_image:
            pushes["base"] = base_image.tag
        if time_image:
            pushes["timestamp"] = time_image.tag
        if latest_image:
            pushes["latest"] = True
        push_log["versions"][version] = pushes

    if options.manifest_add:
        amend_tags = [time_image.tag] + options.manifest_add
        create_and_push_manifest(version, amend_tags)
        if push_latest:
            create_and_push_manifest("latest", amend_tags)

    if options.delete_timestamp_tag:
        remove_image(time_image)


def set_options():
    parser = argparse.ArgumentParser(
        description="Build one or more docker images for clang-ubuntu")
    parser.add_argument(
        "-v", "--version", action="append", required=True,
        help="Use one or more times to specify the versions to run")
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
        "--latest", action="store_true",
        help="Update latest tag. If multiple versions, applies to last one." +
        " If --manifest-add specified will create a latest manifest")
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
    parser.add_argument(
        "--manifest-only", nargs="+",
        help="Create a manifest from the provided timestamp tags, without building." +
        " Will create a manifest for the version and a new timestamp.")
    parser.add_argument(
        "--arch", nargs='?', const='auto', default="",
        help="Architecture string to include in the timestamp tag (e.g. amd64, arm64). If passed without value, it autodetects.")
    parser.add_argument(
        "-l", "--log-file", default="",
        help="json file to log pushes into")

    global options
    options = parser.parse_args()

    if options.manifest_add and len(options.version) > 1:
        raise RuntimeError("Cannot support manifest with multiple versions")

    if options.manifest_only and len(options.version) > 1:
        raise RuntimeError("Cannot support manifest-only with multiple versions")


def run():
    set_options()
    push_log["repo"] = options.repo

    if options.arch == 'auto':
        machine = platform.machine().lower()
        if machine in ['x86_64', 'amd64']:
            options.arch = 'amd64'
        elif machine in ['aarch64', 'arm64']:
            options.arch = 'arm64'
        else:
            options.arch = machine

    for version in options.version:
        latest = options.latest and version == options.version[-1]
        build_one(version, latest)

    if options.log_file:
        with open(options.log_file, "w") as f:
            json.dump(push_log, f)


if __name__ == "__main__":
    run()
