#!/usr/bin/env python

import os
import sys
import time
import pathlib
import unittest
import shutil
import tempfile
import multiprocessing as mp
import logging
from unittest.mock import patch, Mock, call
from unittest import mock

from pyats.datastructures import AttrDict
from pyats.easypy.runinfo import RunInfo
from pyats.easypy.main import EasypyRuntime
from pyats.easypy.reporter.ae import AEReporter
from pyats.easypy.tests.common_mocks import patch_report, unpatch_report
from pyats.easypy.common_funcs import init_runtime
from pyats.reporter.testsuite import TestSuite, Section
from pyats.results import Passed
from pyats.easypy.job import Job

# enforce fork (py38 defaults to spawn in mac)
multiprocessing = mp.get_context('fork')

logger = logging.getLogger(__name__)


class test_GenieJob(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global Job
        from genie.cli.commands.job import GenieJob as Job
    
    def setUp(self):
        sys.modules['pyats.easypy.main']._default_runtime = EasypyRuntime()
        self.runtime = sys.modules['pyats.easypy.main']._default_runtime

        f, self.jobfile = tempfile.mkstemp()
        self.archive_dir = tempfile.mkdtemp(prefix='archive_dir')
        self.runinfo_dir = tempfile.mkdtemp(prefix='runinfo_dir')
        os.close(f)

        with open(self.jobfile, 'w') as f:
            f.write('''
def main():
    pass
''')
        TIME_FORMAT = '%Y%b%d_%H:%M:%S'

        init_runtime(self.runtime, None)
        self.job_uid =  '{name}.{time}'.format(
                                        name = pathlib.Path(self.jobfile).stem,
                                        time = time.strftime(TIME_FORMAT,
                                                           time.localtime()))
        self.runtime.job = AttrDict(jobfile = None, uid = self.job_uid)
        self.runtime.runinfo = RunInfo(archive_dir = self.archive_dir,
                                       runinfo_dir = self.runinfo_dir,
                                       runtime = self.runtime)
        patch_report()
        self.runtime.reporter = AEReporter(runtime = self.runtime)
        self.runtime.reporter.start()
        self.runinfo = self.runtime.runinfo
        self.timestamp = 1575492336.749938
        self.reporter = self.runtime.reporter
    
    def tearDown(self):
        unpatch_report()
        os.remove(self.jobfile)
        shutil.rmtree(self.archive_dir)
        shutil.rmtree(self.runinfo_dir)

    def test_parse_arguments(self):
        self.runtime.plugins._plugins = [Job(runtime=self.runtime)]
        self.runtime.configure_parser()
        args = self.runtime.parse_args(['-testbed_file',
                                        '/path/to/testbedfile.yaml'])
        self.assertIn('-suite_name', self.runtime.parser.format_help())
        self.assertEqual(args.suite_name, None)
        self.assertEqual(args.test_suite, None)
  
if __name__ == '__main__':
    unittest.main()
