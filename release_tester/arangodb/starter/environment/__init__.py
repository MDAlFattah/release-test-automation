#!/usr/bin/env python
""" launch and manage an arango deployment using the starter"""
from enum import Enum
import logging

from typing import Optional
from arangodb.starter.environment.runner import Runner
from arangodb.installers.base import InstallerBase
from arangodb.installers import InstallConfig

class RunnerType(Enum):
    """ dial which runner instance you want"""
    NONE = 0
    LEADER_FOLLOWER = 1
    ACTIVE_FAILOVER = 2
    CLUSTER = 3
    DC2DC = 4


#pylint: disable=import-outside-toplevel
def make_runner(runner_type:RunnerType, baseconfig: InstallConfig, old_inst: InstallerBase , new_inst: Optional[InstallerBase]= None) -> Runner:
    """ get an instance of the arangod runner - as you specify """
    print("get!")

    assert(runner_type)
    assert(baseconfig)
    assert(old_inst)

    logging.debug("Factory for Runner of type: {0}".format(str(runner_type)))
    args = (runner_type, baseconfig, old_inst, new_inst)

    if runner_type == RunnerType.LEADER_FOLLOWER:
        from arangodb.starter.environment.leaderfollower import LeaderFollower
        return LeaderFollower(*args)

    if runner_type == RunnerType.ACTIVE_FAILOVER:
        from arangodb.starter.environment.activefailover import ActiveFailover
        return ActiveFailover(*args)

    if runner_type == RunnerType.CLUSTER:
        from arangodb.starter.environment.cluster import Cluster
        return Cluster(*args)

    if runner_type == RunnerType.DC2DC:
        from arangodb.starter.environment.dc2dc import Dc2Dc
        return Dc2Dc(*args)

    if runner_type == RunnerType.NONE:
        from arangodb.starter.environment.none import NoStarter
        return NoStarter(*args)

    raise Exception("unknown starter type")
