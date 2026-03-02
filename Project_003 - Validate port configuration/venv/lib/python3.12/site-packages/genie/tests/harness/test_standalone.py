import unittest
import subprocess
import re
import os
import yaml
import zipfile

from pyats.results import Passed
from genie.libs.sdk.genie_yamls import datafile
from genie.utils.diff import Diff


class TestStandalone(unittest.TestCase):
    def test_standalone(self):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        p = subprocess.run(
            'pyats run job script/standalone_test_script_job.py '
            '--testbed-file script/testbed.yaml '
            '--trigger-datafile script/trigger_standalone_datafile.yaml '
            '--crft-disable --btrace-disable --disable-device-info '
            '--replay script/mock_device --no-mail --no-upload --speed 2',
            shell=True,
            encoding='utf-8',
            stdout=subprocess.PIPE)
        p1 = re.compile(
            r'^[\w\-: %]+:\s+Success Rate +: +(?P<success_rate>\d+)[.\d ]+%$')
        p1_1 = re.compile(
            r'^[\w\-: %]+:\s+Section Success Rate +: +(?P<success_rate>\d+)[.\d ]+%$')
        p2 = re.compile(
            r'^[\w\-: %]+Creating archive file: (?P<zip_file>.*\.zip)$')
        percent = 0
        section_percent = 0

        for line in p.stdout.splitlines():
            line = line.strip()

            m1 = p1.match(line)
            if m1:
                percent = int(m1.groupdict()['success_rate'])
            m1_1 = p1_1.match(line)
            if m1_1:
                section_percent = int(m1_1.groupdict()['success_rate'])
            m2 = p2.match(line)
            if m2:
                zip_file = m2.groupdict()['zip_file']
        os.chdir(cwd)
        self.assertEqual(percent, 80, p.stdout)
        self.assertEqual(section_percent, 96, p.stdout)

        # check if datafiles exist
        with zipfile.ZipFile(zip_file) as f:
            file_list = f.namelist()
            zip_info = f.infolist()
            # get both trigger_datafile and extended one
            for info in zip_info:
                if info.filename == 'trigger_standalone_datafile.yaml':
                    trigger_datafile = yaml.safe_load(f.read(info.filename))
                if info.filename == 'trigger_standalone_datafile_extended.yaml':
                    trigger_datafile_extended = yaml.safe_load(f.read(info.filename))

        self.assertIn('trigger_standalone_datafile.yaml', file_list)
        self.assertIn('trigger_standalone_datafile_extended.yaml', file_list)
        self.assertIn('verification_datafile_iosxe.yaml', file_list)
        self.assertIn('verification_datafile_iosxe_extended.yaml', file_list)

        # check if based file is in extended file
        with open(datafile('trigger')) as f:
            base_datafile = yaml.safe_load(f.read())

        # check all keys from base_datafile in extended file
        self.assertTrue(set(base_datafile.keys()).issubset(trigger_datafile_extended.keys()))
        # check everything from base_datafile in extended file
        dd = Diff(base_datafile, trigger_datafile_extended, mode='remove')
        dd.findDiff()
        self.assertEqual(str(dd), '')

        # remote zip file
        os.remove(zip_file)


    def test_standalone_config_datafile(self):
        cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        p = subprocess.run(
            'pyats run job script/standalone_basic_script_job.py '
            '--testbed-file script/testbed4.yaml --config-datafile '
            'script/config.yaml --replay script/mock_device --no-mail '
            '--crft-disable --btrace-disable --disable-device-info '
            '--no-upload --speed 2',
            shell=True,
            encoding='utf-8',
            stdout=subprocess.PIPE)
        p1 = re.compile(
            r'Interface +Loopback +0')
        p2 = re.compile(
            r'description +Configured +With +Jinja2 +Config +Datafile')
        p3 = re.compile(
            r'Successfully +applied +the +following +configuration\(s\) +on +device: +uut')
        p4 = re.compile(
            r'script/jin_config.j2')
        check1 = check2 = check3 = check4 = False

        for line in p.stdout.splitlines():
            line = line.strip()

            m = p1.search(line)
            if m:
                check1 = True
            m = p2.search(line)
            if m:
                check2 = True
            m = p3.search(line)
            if m:
                check3 = True
            m = p4.search(line)
            if m:
                check4 = True
        os.chdir(cwd)
        self.assertEqual(all((check1,check2,check3,check4)), True)


    def test_retry_triggers(self):
        """
        To test the retry trigger feature.

        Expected output:
        +------------------------------------------------------------------------------+
        |                             Task Result Details                              |
        +------------------------------------------------------------------------------+
        Task-1: genie_testscript                                                   PASSX
        |-- common_setup                                                          PASSED
        |   |-- connect                                                           PASSED
        |   `-- configure                                                        SKIPPED
        |-- TriggerRetry.uut                                                      FAILED
        |   `-- test                                                              FAILED
        |-- TriggerRetry.uut [Retry 1]                                            FAILED
        |   `-- test                                                              FAILED
        |-- TriggerRetry.uut [Retry 2]                                             PASSX
        |   `-- test                                                              PASSED
        `-- common_cleanup                                                        PASSED
        Done!
        """
        cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        log_contents = subprocess.run(
            'pyats run job script/standalone_retry_trigger_script_job.py '
            '--testbed-file script/testbed.yaml '
            '--trigger-datafile script/standalone_retry_trigger_datafile.yaml '
            '--crft-disable --btrace-disable --disable-device-info '
            '--replay script/mock_device --no-mail --no-upload --speed 2 '
            '--trigger-uids TriggerRetry '
            '--retry retry_wait=2',
            shell=True,
            encoding='utf-8',
            stdout=subprocess.PIPE)
        log_contents = log_contents.stdout
        check1 = check2 = check3 = False

        # TriggerRetry.uut                                                      FAILED
        p1 = re.compile(
            r'TriggerRetry.uut\s+FAILED')
        # TriggerRetry.uut [Retry 1]                                            FAILED
        p2 = re.compile(
            r'TriggerRetry.uut \[Retry 1\]\s+FAILED')
        # TriggerRetry.uut [Retry 2]                                             PASSX
        p3 = re.compile(
            r'TriggerRetry.uut \[Retry 2\]\s+PASSX')

        for line in log_contents.splitlines():
            line = line.strip()
            # TriggerRetry.uut                                                      FAILED
            m = p1.search(line)
            if m:
                check1 = True
            # TriggerRetry.uut [Retry 1]                                            FAILED
            m = p2.search(line)
            if m:
                check2 = True
            # TriggerRetry.uut [Retry 2]                                             PASSX
            m = p3.search(line)
            if m:
                check3 = True
        self.assertEqual(all((check1, check2, check3)), True)

if __name__ == '__main__':
    unittest.main()
