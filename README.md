# clang-ubuntu-docker

Docker images with a versioned Clang/LLVM toolchain installed on Ubuntu, published to
Docker Hub as [teeks99/clang-ubuntu](https://hub.docker.com/r/teeks99/clang-ubuntu).

Packages come from the official [apt.llvm.org](https://apt.llvm.org/) repositories, so each
image is built on the Ubuntu release that LLVM publishes that version for.

## Images

| Clang | Ubuntu base | Built by |
| ----- | ----------- | -------- |
| 15, 16 | `jammy` (22.04) | legacy workflow |
| 17, 18, 19, 20 | `noble` (24.04) | legacy workflow |
| 21, 22 | `resolute` (26.04) | legacy workflow |
| 23 | `resolute` (26.04) | current workflow (also tagged `latest`) |
| 24 | `resolute` (26.04) | pre-release workflow (LLVM development snapshot) |

Older versions (Clang < 15) are no longer built; their Ubuntu bases are out of support.
The `Built by` column rotates as new versions appear — see [Adding a version](#adding-a-version).

Each image installs `build-essential` plus the versioned LLVM packages — `clang`,
`clang-tools`, `clang-format`, `python3-clang`, `libfuzzer`, `lldb`, `lld`, `libc++`,
`libc++abi`, `libomp` and `libunwind`. Clang 16 and later add Polly, libclc, MLIR and the
wasm32/wasm64 runtimes; Clang 21 and later also add `clang-tidy`. BOLT is deliberately left
out because it does not build on aarch64.

Unversioned `clang` and `clang++` symlinks point at the versioned binaries, so both
`clang++` and `clang++-23` work. On the `noble` and `resolute` images the default `ubuntu`
user is removed, leaving UID 1000 free for a user created at runtime.

Images are published for both `linux/amd64` and `linux/arm64`.

```bash
docker run --rm teeks99/clang-ubuntu:23 clang++ --version
```

## Tag patterns

| Tag | Example | What it is |
| --- | ------- | ---------- |
| `latest` | `latest` | Multi-arch manifest for the current stable release (Clang 23) |
| `<version>` | `23` | Multi-arch manifest, moves with each rebuild of that version |
| `<version>_<timestamp>` | `23_20260901_0007` | Immutable multi-arch manifest for one build run |
| `<version>_<arch>_<timestamp>` | `23_amd64_20260901_0004` | The single-arch image a manifest is built from |

Timestamps are UTC, formatted `YYYYMMDD_HHMM`. The per-arch tags are what each builder
pushes; the manifest job then combines them and stamps its own timestamp on the
`<version>_<timestamp>` manifest, so it will differ by a few minutes from the per-arch tags
it references.

Pin `<version>_<timestamp>` for reproducible builds — the `<version>` and `latest` tags are
re-pointed every time the images are rebuilt.

## Building with build_img.py

`build_img.py` drives the whole build/test/tag/push/manifest cycle. It needs Python 3 and a
working `docker` CLI, and shells out to `docker` for everything.

For each requested version it will, by default:

1. `docker build --pull --no-cache` the matching `clang-<version>` directory,
2. smoke test the result inside the container: check that `clang++-<version>`, `clang++` and
   `clang` all report the expected version, then compile and run a hello world with it,
   once with the default standard library and once with `-stdlib=libc++`,
3. apply a timestamp tag,
4. optionally push, and optionally combine per-arch builds into a manifest.

At least one `-v` is required; repeat it to act on several versions. The default repo is
`test/clang`, so without `-r` and `-p` it builds and tags locally without touching Docker
Hub.

```bash
# Build and test one version locally
python build_img.py -v 23

# Build just Clang 22 and 23
python build_img.py -v 22 -v 23

# Build one version and push it to Docker Hub
python build_img.py -v 23 -r teeks99/clang-ubuntu -p

# What CI runs on each builder: push only the arch-stamped timestamp tag
python build_img.py -v 23 -r teeks99/clang-ubuntu -p -T --arch -l amd64_log.json

# Then, once both arches are up, combine them into the manifests
python build_img.py -v 23 -r teeks99/clang-ubuntu --manifest-only 23_amd64_20260901_0004 23_arm64_20260901_0006 --latest
```

### Options

| Option | Effect |
| ------ | ------ |
| `-v`, `--version` | Version to act on; repeat for several. Required. |
| `-r`, `--repo` | Repo to tag and push to. Default `test/clang`; use `teeks99/clang-ubuntu` for Docker Hub. |
| `-p`, `--push` | Push the tags that were created. |
| `--arch [NAME]` | Include an architecture in the timestamp tag. Bare `--arch` autodetects (`amd64`/`arm64`). |
| `--latest` | Also tag/push `latest`. With several versions it applies to the last one; with `--manifest-add`/`--manifest-only` it creates a `latest` manifest. |
| `-T`, `--no-push-tag` | Don't push the bare `<version>` tag, only the timestamp tag. |
| `--no-tag-timestamp` | Skip the timestamp tag, version tag only. |
| `-d`, `--delete-timestamp-tag` | Drop the timestamp tag from the local machine when done. |
| `--no-build` | Skip the build step. |
| `--no-test` | Skip the test step. |
| `--no-force` | Drop `--no-cache`, reuse existing layers. |
| `--no-update-base` | Drop `--pull`, don't re-fetch the Ubuntu base image. |
| `-m`, `--manifest-add` | Build, then create a manifest from this build's timestamp tag plus the tag(s) given here. Single `-v` only. |
| `--manifest-only` | Don't build; create the `<version>` and `<version>_<timestamp>` manifests from the timestamp tags listed. Single `-v` only. |
| `-l`, `--log-file` | Write a JSON record of what was pushed, including the timestamp tag. |

The log file written by `-l` is how the two per-arch CI jobs hand their timestamp tags to
the manifest job:

```json
{"versions": {"23": {"timestamp": "23_amd64_20260901_0004"}}, "repo": "teeks99/clang-ubuntu"}
```

## Automated builds

Three GitHub Actions workflows in [.github/workflows](.github/workflows) build on
`ubuntu-latest` and `ubuntu-24.04-arm`, then join the two into a manifest. All three can
also be started by hand with `workflow_dispatch`, and each one triggers a matching
[teeks99/boost-cpp-docker](https://github.com/teeks99/boost-cpp-docker) build when it
finishes.

| Workflow | Schedule | Versions |
| -------- | -------- | -------- |
| `build-current.yml` | Monthly, 1st at 00:00 UTC | 23, and updates `latest` |
| `build-legacy.yml` | May 1 and Nov 1 | 15–22 |
| `build-prerelease.yml` | Weekly, Sundays | 24 |

## Adding a version

Versions enter as the pre-release build and rotate on from there: the pre-release becomes
the current release, the current release drops back to legacy, and a new directory picks up
the next development snapshot. To add Clang `<n+1>`, where `<n>` is the outgoing
pre-release:

1. Copy `clang-<n>` to `clang-<n+1>` and set `llvmver=<n+1>` in the `Dockerfile`. Leave its
   `llvm.list` on the unsuffixed development repo (`llvm-toolchain-<release> main`) — that
   is the snapshot the pre-release build tracks. If apt.llvm.org has moved to a newer
   Ubuntu release, update the `release` ARG and the release name in `llvm.list` to match.
2. Add the `-<n>` suffix to `clang-<n>/llvm.list`, making it
   `llvm-toolchain-<release>-<n> main`. Now that `<n>` is released it has a repo of its
   own, and the unsuffixed one has moved on to `<n+1>`.
3. Rotate the workflows, which are the only place versions are listed:
   - [`build-prerelease.yml`](.github/workflows/build-prerelease.yml): set `CLANG_VERSION`
     to `<n+1>`.
   - [`build-current.yml`](.github/workflows/build-current.yml): set `CLANG_VERSION` to
     `<n>`. This is the build that also pushes `latest`.
   - [`build-legacy.yml`](.github/workflows/build-legacy.yml): append the version
     `build-current.yml` was previously building to the `versions` array in the
     `set-versions` step.
4. Update the [Images](#images) and [Automated builds](#automated-builds) tables above.

`build_img.py` needs no changes — it builds whatever versions `-v` names.

## License

MIT — see [LICENSE](LICENSE).
