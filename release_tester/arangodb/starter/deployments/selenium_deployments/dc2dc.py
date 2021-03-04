#!/usr/bin/env python3
""" test the UI of a leader follower setup """
from sbase import SeleniumRunner

class LeaderFollower(SeleniumRunner):
    """ check the leader follower setup and its properties """
    def __init__(self, webdriver):
        super().__init__(webdriver)
