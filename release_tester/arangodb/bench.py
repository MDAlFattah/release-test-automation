#!/usr/bin/env python
""" Manage one instance of the arangobench
"""

import pathlib

import psutil
import yaml

import tools.loghelper as lh

BENCH_TODOS = {}
def load_scenarios():
    """ load the yaml testcases """
    yamldir = pathlib.Path(__file__).parent.absolute() / '..' / '..' / 'scenarios' / 'arangobench'
    for one_yaml in yamldir.iterdir():
        if one_yaml.is_file():
            with open(one_yaml) as fileh:
                BENCH_TODOS[one_yaml.name[:-4]] = yaml.load(fileh, Loader=yaml.Loader)

class ArangoBenchManager():
    """ manages one arangobackup instance"""
    def __init__(self, basecfg, connect_instance):
        self.connect_instance = connect_instance

        self.cfg = basecfg
        self.moreopts = [
            '--server.endpoint', self.connect_instance.get_endpoint(),
            '--server.username', str(self.cfg.username),
            '--server.password', str(self.cfg.passvoid),
            '--server.connection-timeout', '10',
            # else the wintendo may stay mute:
            '--log.force-direct', 'true', '--log.foreground-tty', 'true'
        ]
        if self.cfg.verbose:
            self.moreopts += ["--log.level=debug"]

        self.username = 'testuser'
        self.passvoid = 'testpassvoid'
        self.instance = None

    def launch(self, testcase_no):
        """ run arangobench """
        testcase = BENCH_TODOS[testcase_no]
        arguments = [self.cfg.bin_dir / 'arangobench'] + self.moreopts
        for key in testcase.keys():
            arguments.append('--' + key)
            arguments.append(str(testcase[key]))

        if self.cfg.verbose:
            lh.log_cmd(arguments)

        self.instance = psutil.Popen(arguments)
        print("az"*40)

    def wait(self):
        """ wait for our instance to finish """
        self.instance.wait()
