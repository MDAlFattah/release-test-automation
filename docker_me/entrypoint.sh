#!/bin/bash -x

cd /home/test/release-test-automation
find
set

python3 release_tester/perf.py --version 3.8.0-devel --no-enterprise --package-dir /tmp/ --frontends $COORDINATOR_1 --frontends $COORDINATOR_2 --frontends $COORDINATOR_3 --mode tests --verbose
