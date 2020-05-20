#!/usr/bin/env python
""" Run a javascript command by spawning an arangosh
    to the configured connection """
import logging
import psutil
import tools.loghelper as lh
import subprocess

class ArangoshExecutor():
    """ configuration """
    def __init__(self, config):
        self.cfg = config

    def run_command(self, cmd, verbose = True):
        """ launch a command, print its name """
        run_cmd = [self.cfg.bin_dir / "arangosh",
                   "--server.endpoint",
                   "tcp://127.0.0.1:{cfg.port}".format(cfg=self.cfg),
                   "--server.username", str(self.cfg.username),
                   "--server.password", str(self.cfg.passvoid),
                   "--javascript.execute-string", str(cmd[1])
                  ]
        if len(cmd) > 2:
            run_cmd += cmd[2:]

        arangosh_run = None
        if verbose:
            lh.log_cmd(run_cmd)
            arangosh_run = psutil.Popen(run_cmd)
        else:
            arangosh_run = psutil.Popen(run_cmd, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

        exitcode = arangosh_run.wait(timeout=30)
        logging.debug("exitcode {0}".format(exitcode))
        return exitcode == 0

    def self_test(self):
        """ run a command that throws to check exit code handling """
        logging.info("running version check")
        res = self.run_command((
            'check throw exit codes',
            "throw 'yipiahea motherfucker'"))
        logging.debug("sanity result: " + str(res))
        if res:
            raise Exception("arangosh doesn't exit with non-0 to indicate errors")

    def run_script(self, cmd, verbose = True):
        """ launch an external js-script, print its name """
        run_cmd = [self.cfg.bin_dir / "arangosh",
                   "--server.endpoint",
                   "tcp://127.0.0.1:{cfg.port}".format(cfg=self.cfg),
                   "--server.username", str(self.cfg.username),
                   "--server.password", str(self.cfg.passvoid),
                   "--javascript.execute", str(cmd[1])
                  ]

        if len(cmd) > 2:
            run_cmd += cmd[2:]

        arangosh_run = None
        if verbose:
            lh.log_cmd(run_cmd)
            arangosh_run = psutil.Popen(run_cmd)
        else:
            arangosh_run = psutil.Popen(run_cmd, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)

        exitcode = arangosh_run.wait(timeout=30)
        logging.debug("exitcode {0}".format(exitcode))
        return exitcode == 0

    def js_version_check(self):
        """ run a version check command; this can double as password check """
        logging.info("running version check")
        res = self.run_command((
            'check version',
            "if (db._version()!='%s') { throw 'version check failed - ' + db._version() + '!= %s'}" % (self.cfg.version, self.cfg.version)))
        logging.debug("version check result: " + str(res))
        return res

    def create_test_data(self, testname):
        """ deploy testdata into the instance """
        if testname:
            logging.info("adding test data for {0}".format(testname))
        else:
            logging.info("adding test data")

        return self.run_script([
            'setting up test data',
            self.cfg.test_data_dir / 'makedata.js'])

    def check_test_data(self, testname):
        """ check back the testdata in the instance """
        if testname:
            logging.info("checking test data for {0}".format(testname))
        else:
            logging.info("checking test data")

        self.run_script([
            'checking test data integrity',
            self.cfg.test_data_dir / 'checkdata.js'])

    def clear_test_data(self, testname):
        """ flush the testdata from the instance again """
        if testname:
            logging.info("removing test data for {0}".format(testname))
        else:
            logging.info("removing test data")

        self.run_script([
            'cleaning up test data',
            self.cfg.test_data_dir / 'cleardata.js'])
