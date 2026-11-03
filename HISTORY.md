# Changelog


## 2.1.1 (2026-08-14)

### Added

* Schedule Actions cache purge every 3 days. [Luis Alejandro Martínez Faneyth]


### Changed

* Document example workflows on ubuntu-24.04. [Luis Alejandro Martínez Faneyth]


### Other

* Fix(ci): smoke-test action runtime image tagged :test. [Cursor Agent]

* Chore: rebuild develop image with agoras-meta data fix. [Luis Alejandro Martínez Faneyth]


## 2.1.0 (2026-08-07)

### Added

* Document gitchangelog commit tags and fix HISTORY.md release notes awk. [Luis Alejandro Martínez Faneyth]


### Fixed

* Add docstrings, fix pyright narrowing, and add libatomic1 for pyright. [Luis Alejandro Martínez Faneyth]

* Tag test image as :test to avoid overwriting dev image. [Luis Alejandro Martínez Faneyth]

* Fixing docker image bug. [Luis Alejandro Martínez Faneyth]

* Retry transient GitHub API errors in PR auto-merge. [Luis Alejandro Martínez Faneyth]

* Fixing content file argument name. [Luis Alejandro Martínez Faneyth]

* Use top-level getOctokit in pr-auto-merge updateBranch step. [Luis Alejandro Martínez Faneyth]


### Other

* Fix(ci): pin setup-python v7 SHA and add PyYAML to tox coverage deps. [Cursor Agent]

* Fix(ci): add PyYAML to tox coverage deps for test_execute imports. [Cursor Agent]

* Fix(ci): add PyYAML to tox coverage test dependencies. [Cursor Agent]

* Add thread action support for x, threads, and discord. [Luis Alejandro Martínez Faneyth]

* Upgrade PR auto-merge to SHA-bound native-first controller. [Luis Alejandro Martínez Faneyth]

* Fix: replace deluser/delgroup with userdel/groupdel in Dockerfiles. [Luis Alejandro Martínez Faneyth]

* Chore: apply rosey-maintainer fleet sync. [Luis Alejandro Martínez Faneyth]

* Chore: update gitignore. [Luis Alejandro Martínez Faneyth]

* Fix(docker): add -y flag to apt-get install and use python3-venv. [Luis Alejandro Martínez Faneyth]

* WIP: local changes before sync. [Luis Alejandro Martínez Faneyth]

* Update. [Luis Alejandro Martínez Faneyth]

* Fixing build. [Luis Alejandro Martínez Faneyth]

* Bump. [Luis Alejandro Martínez Faneyth]

* Removing unnecessary vars. [Luis Alejandro Martínez Faneyth]

* Fix(ci): use env var for github.ref in push workflow run step. [Cursor Agent]

* Feat: support linkedin-access-token input for standard LinkedIn apps. [Luis Alejandro Martínez Faneyth]

* Feat(action): add refresh-credentials GitHub secrets sync. [Luis Alejandro Martínez Faneyth]

* Fix: skip auto-merge for draft pull requests. [Luis Alejandro Martínez Faneyth]

* Chore: maintainer sync follow-ups for env, docs, and Makefile. [Luis Alejandro Martínez Faneyth]

* Chore: sync maintainer ops from rosey-maintainer-sync. [Luis Alejandro Martínez Faneyth]

* Chore: sync maintainer ops from fleet-wide rosey-maintainer-sync. [Luis Alejandro Martínez Faneyth]

* Adapting agoras-actions to new version of agoras. [Luis Alejandro Martínez Faneyth]

* Chore: sync maintainer release workflow (checkout@v7) [Luis Alejandro Martínez Faneyth]

* Chore: sync maintainer ops and track README version in bumpversion. [Luis Alejandro Martínez Faneyth]


## 2.0.5 (2026-06-24)

### Other

* Add execute handoff regression tests and wire agoras into tox CI. [Luis Alejandro Martínez Faneyth]


## 2.0.4 (2026-06-24)

### Other

* Fix agoras CLI hand-off import in execute.py. [Luis Alejandro Martínez Faneyth]


## 2.0.2 (2026-06-24)

### Other

* Fixing misalignment versions bug. [Luis Alejandro Martínez Faneyth]

* Fix: restore GHCR 1.1.3 image and guard push version pins. [Luis Alejandro Martínez Faneyth]

* Chore: export BASH_ENV in Makefile for bash recipe env. [Luis Alejandro Martínez Faneyth]

* Fix: one-line post_bump_commands for bumpversion compatibility. [Luis Alejandro Martínez Faneyth]


## 2.0.1 (2026-06-23)

### Other

* Chore: sync maintainer ops and inline post_bump_commands parser. [Luis Alejandro Martínez Faneyth]

* Chore: sync maintainer release scripts and CI workflows. [Luis Alejandro Martínez Faneyth]

* Chore: maintainer sync toolkit 0.4.3. [Luis Alejandro Martínez Faneyth]

* Update. [Luis Alejandro Martínez Faneyth]

* Chore: maintainer sync toolkit 0.4.2 — PR CI + auto-merge. [Luis Alejandro Martínez Faneyth]

* Add .cursorrules with Cursor Cloud dev environment instructions. [Cursor Agent]

* Chore: sync PR auto-merge, CodeQL PR gate, and maintainer files from rosey-maintain. [Luis Alejandro Martínez Faneyth]


## 2.0.0 (2026-06-21)

### Other

* Fixing build. [Luis Alejandro Martínez Faneyth]

* Improving maintainer files. [Luis Alejandro Martínez Faneyth]

* Preparing release. [Luis Alejandro Martínez Faneyth]

* Preparing release. [Luis Alejandro Martínez Faneyth]

* Chore: fleet release parity — gates, dependabot, hotfix removal. [Luis Alejandro Martínez Faneyth]

* Apply rosey maintainer fleet sync. [Luis Alejandro Martínez Faneyth]

* Adding bumpversion config. [Luis Alejandro Martínez Faneyth]

* Release Agoras Actions 2.0 with PyPI-based installs and native CLI routing. [Luis Alejandro Martínez Faneyth]

* Improving gitignore. [Luis Alejandro Martínez Faneyth]

* Update keepalive.yml. [Luis Alejandro]


## 1.1.3 (2023-09-05)

### Changed

* Adding support for --status-link. [Luis Alejandro Martínez Faneyth]


## 1.1.2 (2023-09-03)

### Fixed

* Fixing ourput name. [Luis Alejandro Martínez Faneyth]


## 1.1.1 (2023-09-01)

### Changed

* Improving readme. [Luis Alejandro Martínez Faneyth]

* Improving general quality of action. [Luis Alejandro Martínez Faneyth]

* Fixing workflow build. [Luis Alejandro Martínez Faneyth]

* Fixing workflow build. [Luis Alejandro Martínez Faneyth]

* Fixing workflow build. [Luis Alejandro Martínez Faneyth]

* Fixing workflow build. [Luis Alejandro Martínez Faneyth]

* Fixing workflow build. [Luis Alejandro Martínez Faneyth]

* Fixing yaml syntax error. [Luis Alejandro Martínez Faneyth]

* Creating action scripts. [Luis Alejandro Martínez Faneyth]

* Improving documentation. [Luis Alejandro Martínez Faneyth]

* Improving Readme. [Luis Alejandro Martínez Faneyth]

* Changing name to agoras. [Luis Alejandro Martínez Faneyth]

* Renaming to Agora. [Luis Alejandro Martínez Faneyth]

* Moving main functionality to sacli project. [Luis Alejandro Martínez Faneyth]

* Removing unused code. [Luis Alejandro Martínez Faneyth]

* Adding actions config. [Luis Alejandro Martínez Faneyth]


### Fixed

* Fixin action.yml for publishing on marketplace. [Luis Alejandro Martínez Faneyth]

* Fixing image build. [Luis Alejandro Martínez Faneyth]

* Fixing actions. [Luis Alejandro Martínez Faneyth]


### Other

* Initial commit. [Luis Alejandro Martínez Faneyth]

