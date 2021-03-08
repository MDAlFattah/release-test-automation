#!/usr/bin/env python3
""" test the UI of a leader follower setup """
import time
from arangodb.starter.deployments.selenium_deployments.sbase import SeleniumRunner

class Cluster(SeleniumRunner):
    """ check the leader follower setup and its properties """
    def __init__(self, webdriver):
        super().__init__(webdriver)

    def check_old(self, cfg):
        """ check the integrity of the old system before the upgrade """
        self.detect_version(cfg)
        self.navbar_goto('nodes')
        time.sleep(3)
        self.navbar_goto('cluster')
        time.sleep(3)
        print(self.cluster_dashboard_get_count())
        self.check_health_state('NODES OK')
