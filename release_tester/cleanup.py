#!/usr/bin/env python3

""" Release testing script"""
import logging
from pathlib import Path
import sys
from tools.killall import kill_all_processes
from arangodb.installers import make_installer, InstallerConfig
from arangodb.starter.deployments import RunnerType, make_runner
import tools.loghelper as lh

logging.basicConfig(
    level=logging.DEBUG,
    datefmt='%H:%M:%S',
    format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s'
)

def run_test():
    """ main """
    logging.getLogger().setLevel(logging.DEBUG)

    install_config = InstallerConfig('0.0',
                                     True,
                                     False,
                                     Path("/tmp/"),
                                     "",
                                     False)
    inst = make_installer(install_config)

    kill_all_processes()
    inst.load_config()
    inst.cfg.interactive = False
    inst.stop_service()
    starter_mode = [RunnerType.LEADER_FOLLOWER,
                    RunnerType.ACTIVE_FAILOVER,
                    RunnerType.CLUSTER]#,
                    #RunnerType.DC2DC] here __init__ will create stuff, TODO.
    for runner_type in starter_mode:
        assert(runner_type)

        runner = make_runner(runner_type, inst.cfg, inst, None)
        runner.cleanup()

    inst.un_install_package()
    inst.cleanup_system()


if __name__ == "__main__":
    run_test()
