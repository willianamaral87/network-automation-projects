
import os
import re
import sys
import json 
import shutil
import logging 
import tempfile
import unittest

from io import StringIO
from pathlib import Path
from contextlib import redirect_stdout
from contextlib import redirect_stderr

from pyats.cli.utils import cmd
from pyats.cli.__main__ import main as entrypoint_main
from genie.cli.commands.develop import DevelopCommand
from genie.cli.commands.undevelop import UndevelopCommand

# Set up internal logger
log = logging.getLogger(__name__)

# Don't sort test alphabetically
unittest.TestLoader.sortTestMethodsUsing = None

temp_dir = None

def package_is_installed(package_name, pip_list_output_as_json):
    ''' Returns True if the named package is in development mode'''
    for pkg in json.loads(pip_list_output_as_json):
        if pkg['name'] == package_name:
            return True
    return False

def get_installed_pip_packages_as_json(path_to_pip_binary=None, 
                                       dev_mode_packages_only=False, 
                                       exclude_dev_mode_packages = False):
    ''' Returns output of pip list --format json'''

    if dev_mode_packages_only:
        pkg_modifier = '-e'
    elif exclude_dev_mode_packages:
        pkg_modifier = '--exclude-editable'
    else:
        pkg_modifier = ''

    cmd_output = \
        cmd('%s list %s --format json' % (path_to_pip_binary, pkg_modifier))
    x = re.match(r'.*(\[.*\]).*', cmd_output).groups()[0]
    return x

def create_temp_dir():
    ''' Creates a temporary directory with an identifiable prefix'''
    global temp_dir
    try:
        temp_dir = tempfile.mkdtemp(prefix='test_develop_')
    except Exception:
        log.exception("Error during temp directory creation")
        raise

def delete_temp_directory(directory):
    ''' Deletes the specified directory '''
    log.debug("Deleting directory %s" % directory)
    try:
        shutil.rmtree(directory)
    except Exception:
        log.exception("Unexpected error during removal of temp directory")
        raise
    else:
        log.debug("Directory deleted successfully")


class Test_DevelopUndevelopCommand(unittest.TestCase):

    default_pkg_data = {
        "cisco-distutils": {"repo_name": "ciscodistutils"},
        "genie": {"repo_name": "genie"},
        "genie.libs": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
            "related_pkgs": [
                "genie.libs.clean",
                "genie.libs.conf",
                "genie.libs.filetransferutils",
                "genie.libs.ops",
                "genie.libs.health",
                "genie.libs.robot",
                "genie.libs.sdk",
            ],
        },
        "genie.libs.clean": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.conf": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.filetransferutils": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.health": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.ops": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.robot": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.sdk": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.parser": {
            "url": "https://github.com/CiscoTestAutomation/genieparser.git",
            "repo_name": "genieparser",
        },
        "genie.telemetry": {
            "url": "https://github.com/CiscoTestAutomation/genietelemetry.git",
            "repo_name": "genietelemetry",
        },
        "genie.trafficgen": {
            "url": "https://github.com/CiscoTestAutomation/genietrafficgen.git",
            "repo_name": "genietrafficgen",
        },
        "pyats": {"repo_name": "pyats"},
        "pyats.contrib": {
            "url": "https://github.com/CiscoTestAutomation/pyats.contrib.git",
            "repo_name": "pyats.contrib",
        },
        "rest.connector": {
            "url": "https://github.com/CiscoTestAutomation/rest.git",
            "repo_name": "rest",
        },
        "unicon": {"repo_name": "unicon"},
        "unicon.plugins": {
            "url": "https://github.com/CiscoTestAutomation/unicon.plugins.git",
            "repo_name": "unicon.plugins",
        },
        "yang.connector": {
            "url": "https://github.com/CiscoTestAutomation/yang.git",
            "repo_name": "yang",
        },
    }  

    internal_pkg_data = {
        "cisco-distutils": {
            "repo_name": "ciscodistutils",
            "url": "git@wwwin-github.cisco.com:pyATS/ciscodistutils.git",
        },
        "genie": {
            "repo_name": "genie",
            "url": "git@wwwin-github.cisco.com:pyATS/genie.git",
        },
        "genie.libs": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
            "related_pkgs": [
                "genie.libs.clean",
                "genie.libs.conf",
                "genie.libs.filetransferutils",
                "genie.libs.ops",
                "genie.libs.health",
                "genie.libs.robot",
                "genie.libs.sdk",
            ],
        },
        "genie.libs.clean": {
            "url": "git@wwwin-github.cisco.com:pyATS/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.conf": {
            "url": "git@wwwin-github.cisco.com:pyATS/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.filetransferutils": {
            "url": "git@wwwin-github.cisco.com:pyATS/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.health": {
            "url": "git@wwwin-github.cisco.com:pyATS/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.ops": {
            "url": "git@wwwin-github.cisco.com:pyATS/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.robot": {
            "url": "git@wwwin-github.cisco.com:pyATS/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.sdk": {
            "url": "git@wwwin-github.cisco.com:pyATS/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.parser": {
            "url": "git@wwwin-github.cisco.com:pyATS/genieparser.git",
            "repo_name": "genieparser",
        },
        "genie.telemetry": {
            "url": "git@wwwin-github.cisco.com:pyATS/genietelemetry.git",
            "repo_name": "genietelemetry",
        },
        "genie.trafficgen": {
            "url": "git@wwwin-github.cisco.com:pyATS/genietrafficgen.git",
            "repo_name": "genietrafficgen",
        },
        "pyats": {
            "repo_name": "pyats",
            "url": "git@wwwin-github.cisco.com:pyATS/pyats.git",
            "related_pkgs": [
                "ats",
                "ats.aereport",
                "ats.aetest",
                "ats.async",
                "ats.cisco",
                "ats.connections",
                "ats.datastructures",
                "ats.easypy",
                "ats.kleenex",
                "ats.log",
                "ats.reporter",
                "ats.results",
                "ats.robot",
                "ats.tcl",
                "ats.topology",
                "ats.utils",
                "cisco-distutils",
            ],
        },
        "pyats.contrib": {
            "url": "https://github.com/CiscoTestAutomation/pyats.contrib.git",
            "repo_name": "pyats.contrib",
        },
        "rest.connector": {
            "url": "https://github.com/CiscoTestAutomation/rest.git",
            "repo_name": "rest",
        },
        "unicon": {
            "repo_name": "unicon",
            "url": "git@wwwin-github.cisco.com:pyATS/unicon.git",
        },
        "unicon.plugins": {
            "url": "git@wwwin-github.cisco.com:pyATS/unicon.plugins.git",
            "repo_name": "unicon.plugins",
        },
        "yang.connector": {
            "url": "https://github.com/CiscoTestAutomation/yang.git",
            "repo_name": "yang",
        },
    }

    external_pkg_data = {
        "genie.libs": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
            "related_pkgs": [
                "genie.libs.clean",
                "genie.libs.conf",
                "genie.libs.filetransferutils",
                "genie.libs.ops",
                "genie.libs.health",
                "genie.libs.robot",
                "genie.libs.sdk",
            ],
        },
        "genie.libs.clean": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.conf": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.filetransferutils": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.health": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.ops": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.robot": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.sdk": {
            "url": "https://github.com/CiscoTestAutomation/genielibs.git",
            "repo_name": "genielibs",
        },
        "genie.libs.parser": {
            "url": "https://github.com/CiscoTestAutomation/genieparser.git",
            "repo_name": "genieparser",
        },
        "genie.telemetry": {
            "url": "https://github.com/CiscoTestAutomation/genietelemetry.git",
            "repo_name": "genietelemetry",
        },
        "genie.trafficgen": {
            "url": "https://github.com/CiscoTestAutomation/genietrafficgen.git",
            "repo_name": "genietrafficgen",
        },
        "pyats.contrib": {
            "url": "https://github.com/CiscoTestAutomation/pyats.contrib.git",
            "repo_name": "pyats.contrib",
        },
        "rest.connector": {
            "url": "https://github.com/CiscoTestAutomation/rest.git",
            "repo_name": "rest",
        },
        "unicon.plugins": {
            "url": "https://github.com/CiscoTestAutomation/unicon.plugins.git",
            "repo_name": "unicon.plugins",
        },
        "yang.connector": {
            "url": "https://github.com/CiscoTestAutomation/yang.git",
            "repo_name": "yang",
        },
    }

    @classmethod
    def setUpClass(cls):
        sys.modules['pyats.cli.core'].StreamHandler = logging.StreamHandler
        create_temp_dir()

    @classmethod
    def tearDownClass(cls):
        global temp_dir
        delete_temp_directory(temp_dir)

    def setUp(self):
        logging.root.setLevel(logging.DEBUG)
        logging.root.handlers.clear()
        self.maxDiff = None
        self.develop_command = DevelopCommand(prog=None)
        self.undevelop_command = UndevelopCommand(prog=None)

    def assert_pkgs_in_dev_mode(self, list_of_packages, pip_binary):
        pip_data_json = \
            get_installed_pip_packages_as_json(pip_binary, 
                                               dev_mode_packages_only=True)
        for package in list_of_packages:
            self.assertTrue(package_is_installed(package, pip_data_json))

    def assert_pkgs_not_in_dev_mode(self, list_of_packages, pip_binary):
        pip_data_json = \
            get_installed_pip_packages_as_json(pip_binary, 
                                               dev_mode_packages_only=True)
        for package in list_of_packages:
            self.assertFalse(package_is_installed(package, pip_data_json))

    def assert_pkgs_installed(self, list_of_packages, pip_binary): 
        pip_data_json = \
            get_installed_pip_packages_as_json(pip_binary, 
                                               exclude_dev_mode_packages=True)
        for package in list_of_packages:
            self.assertTrue(package_is_installed(package, pip_data_json))

    def assert_pkgs_not_installed(self, list_of_packages, pip_binary): 
        pip_data_json = \
            get_installed_pip_packages_as_json(pip_binary, 
                                               exclude_dev_mode_packages=True)
        for package in list_of_packages:
            self.assertFalse(package_is_installed(package, pip_data_json))

    def assert_is_git_repo(self, directory):
        self.assertTrue(os.path.isdir(os.path.join(directory, ".git")))

    def assert_is_internal_repo(self, repo_dir):
        cmd_output = cmd('git -C %s remote get-url origin' % (repo_dir))
        self.assertTrue(cmd_output.startswith('git@'))

    def assert_is_external_repo(self, repo_dir):
        cmd_output = cmd('git -C %s remote get-url origin' % (repo_dir))
        self.assertTrue(cmd_output.startswith('https'))


    def test_is_internal_installation(self):
        self.assertTrue(
            self.develop_command.is_internal_installation(
                working_set_list=['ats.cisco']))
        self.assertFalse(
            self.develop_command.is_internal_installation(
                working_set_list=['pyats.cisco']))
    

    def test_rebuild_pkg_data(self):
        rebuilt_internal_pkg_data = \
            self.develop_command.rebuild_pkg_data(self.default_pkg_data, 
                                                  internal_installation=True)
        self.assertDictEqual(self.internal_pkg_data, rebuilt_internal_pkg_data)

        rebuilt_external_pkg_data = \
            self.develop_command.rebuild_pkg_data(self.default_pkg_data, 
                                                  internal_installation=False)
        self.assertDictEqual(self.external_pkg_data, rebuilt_external_pkg_data)


    def test_rebuild_package_list(self):

        all_internal_packages = [
            'cisco-distutils', 'genie', 'genie.libs.clean', 'genie.libs.conf', 
            'genie.libs.filetransferutils', 'genie.libs.health', 
            'genie.libs.ops', 'genie.libs.parser', 'genie.libs.robot', 
            'genie.libs.sdk', 'genie.telemetry', 'genie.trafficgen', 'pyats', 
            'pyats.contrib', 'rest.connector', 'unicon', 'unicon.plugins', 
            'yang.connector'
        ]

        all_external_packages = [
            'genie.libs.clean', 'genie.libs.conf', 
            'genie.libs.filetransferutils', 'genie.libs.health', 
            'genie.libs.ops', 'genie.libs.parser', 'genie.libs.robot', 
            'genie.libs.sdk', 'genie.telemetry', 'genie.trafficgen',
            'pyats.contrib', 'rest.connector', 'unicon.plugins', 
            'yang.connector'
        ]

        genielibs_packages = [
            'genie.libs.clean', 'genie.libs.conf', 
            'genie.libs.filetransferutils', 'genie.libs.health', 
            'genie.libs.ops',  'genie.libs.robot', 'genie.libs.sdk'
        ]

        # Test 'all' for internal installation
        actual_packages_list = \
            self.develop_command.rebuild_package_list(['all'], 
                                                      self.internal_pkg_data)
        self.assertListEqual(all_internal_packages, actual_packages_list)

        # Test 'all' for external installation
        actual_packages_list = \
            self.develop_command.rebuild_package_list(['all'], 
                                                      self.external_pkg_data)
        self.assertListEqual(all_external_packages, actual_packages_list)

        # Test 'genie.libs' expands into correct subpackages 
        # internally and externally
        actual_packages_list = \
            self.develop_command.rebuild_package_list(['genie.libs'], 
                                                      self.internal_pkg_data)
        self.assertListEqual(genielibs_packages, actual_packages_list)
        
        actual_packages_list = \
            self.develop_command.rebuild_package_list(['genie.libs'], 
                                                      self.external_pkg_data)
        self.assertListEqual(genielibs_packages, actual_packages_list)

        # Test that duplicates are removed from package list
        actual_packages_list = \
            self.develop_command.rebuild_package_list(
                ['genie.libs', 'all', 'genie.libs', 'genie.libs.parser'], 
                self.internal_pkg_data)
        self.assertListEqual(all_internal_packages, actual_packages_list)


    def test_check_requested_packages_validity(self):
        # Test that at least one package must be supplied
        with self.assertRaises(Exception) as cm:
            self.develop_command.check_requested_packages_validity(list(), 
                                                                   dict())
        self.assertIn("Please specify at least one package to put into "
                      "development mode", str(cm.exception))

        # Test that wrong package name will raise an Exception
        pkg = 'invalid'
        with self.assertRaises(Exception) as cm:
            self.develop_command.\
                check_requested_packages_validity([pkg], self.internal_pkg_data)
        self.assertIn("Package %s is not an available choice for the current "
                      "installation mode." % pkg, str(cm.exception))

        # Test that internal only package names will not be shown for external 
        # installation
        internal_only_packages = ['genie', 'pyats', 'unicon', 'cisco-distutils']
        for pkg in internal_only_packages:
            with self.assertRaises(Exception) as cm:
                self.develop_command.\
                    check_requested_packages_validity([pkg], 
                                                      self.external_pkg_data)
            self.assertIn(
"""all
    genie.libs
    genie.libs.clean
    genie.libs.conf
    genie.libs.filetransferutils
    genie.libs.health
    genie.libs.ops
    genie.libs.robot
    genie.libs.sdk
    genie.libs.parser
    genie.telemetry
    genie.trafficgen
    pyats.contrib
    rest.connector
    unicon.plugins
    yang.connector""", str(cm.exception))

    def test_create_and_delete_directory(self):

        # Store current working directory prior to test. Re-establish after
        pre_cwd = os.getcwd()

        # Test with an absolute path and a relative path
        with tempfile.TemporaryDirectory() as temp_directory:

            test_dir = os.path.join(temp_directory, 'test')

            # Create and delete directory using absolute path
            created_directory = self.develop_command.create_directory(test_dir)
            self.assertTrue(os.path.isdir(created_directory))

            self.develop_command.delete_directory(created_directory, pkg='')
            self.assertFalse(os.path.isdir(created_directory))

            # Create and delete directory using relative path
            os.chdir(temp_directory)
            created_directory = self.develop_command.create_directory('test')
            self.assertTrue(os.path.isdir(os.path.join(temp_directory, 'test')))
            self.assertTrue(os.path.isdir(created_directory))

            self.develop_command.delete_directory(created_directory, pkg='')
            self.assertFalse(os.path.isdir(created_directory))

            # Test that dir does not get deleted if dir_deleted flag is True
            self.develop_command.GENIELIBS_FLAGS['dir_deleted'] = True
            self.develop_command.delete_directory(temp_directory, 
                                                  pkg='genie.libs.sdk')
            self.assertTrue(os.path.isdir(temp_directory))
        
        # Re-establish current working directory to what it was originally
        os.chdir(pre_cwd)

    def test_clone_repo(self):
        # Test a public repo is cloned successfully
        with tempfile.TemporaryDirectory() as temp_dir:
            pkg_to_clone = 'rest.connector'
            ret_value = \
                self.develop_command.clone_repo(pkg_to_clone, 
                                                self.external_pkg_data, 
                                                temp_dir)
            self.develop_command.check_git_repo_validity(temp_dir)
            self.assertTrue(ret_value)

        # Test genie.libs repo is not cloned if GENIELIBS_FLAGS['repo_cloned']
        # flag is already set
        with tempfile.TemporaryDirectory() as temp_dir:
            pkg_to_clone = 'genie.libs.sdk'
            self.develop_command.GENIELIBS_FLAGS['repo_cloned'] = True
            ret_value = \
                self.develop_command.clone_repo(pkg_to_clone, 
                                                self.external_pkg_data, 
                                                temp_dir)
            self.assertFalse(ret_value)

    def test_is_pkg_part_of_genielibs(self):
        # return pkg.startswith('genie.libs') and pkg != 'genie.libs.parser'
        self.assertTrue(self.develop_command\
            .is_pkg_part_of_genielibs('genie.libs.conf'))
        self.assertTrue(self.develop_command\
            .is_pkg_part_of_genielibs('genie.libs.clean'))
        self.assertTrue(self.develop_command\
            .is_pkg_part_of_genielibs('genie.libs.sdk'))
        self.assertFalse(self.develop_command\
            .is_pkg_part_of_genielibs('genie.libs.parser'))
        self.assertFalse(self.develop_command\
            .is_pkg_part_of_genielibs('unicon'))
        self.assertFalse(self.develop_command\
            .is_pkg_part_of_genielibs('genie'))

    def test_reinsert_genielibs_pkgs(self):
        cur_pkg = 'genie.libs.health'
        packages = ['genie.libs.ops', 'genie.libs.sdk', 'pyats.contrib']
        successful_packages = \
            ['genie.libs.conf', 'genie.libs.clean', 'genie.libs.parser']

        expected_packages = ['genie.libs.clean','genie.libs.conf', 
                             'genie.libs.health', 'genie.libs.ops', 
                             'genie.libs.sdk', 'pyats.contrib']

        ammended_pkg_list, successful_packages = \
            self.develop_command.reinsert_genielibs_pkgs(cur_pkg, 
                                                         packages, 
                                                         successful_packages)

        self.assertListEqual(expected_packages, ammended_pkg_list)
        self.assertListEqual(['genie.libs.parser'], successful_packages)


    def test_develop_help(self):

        temp_stdout = StringIO()
        with redirect_stdout(temp_stdout):
            try:
                entrypoint_main(['develop', '--help'])
            except SystemExit:
                pass

        part1 = '''
Usage:
  pyats develop [packages...] [options]
  
Usage Examples:
  pyats develop all
  pyats develop genie.libs.sdk --skip-version-check
  pyats develop genie.libs.parser genie.trafficgen --external
  pyats develop unicon.plugins genie.libs --delete-repos --directory my_repos
  pyats develop pyats.config --clone-only

Description:
  Puts listed pyATS packages into development mode. Listed packages will have 
  their repositories downloaded from Github if required and 'make develop' will be 
  run for each package. By default, internal Cisco repos will be cloned if the 
  pyATS installation is internal, otherwise external repos will be cloned instead. 
  Github SSH keys are required to clone internal Cisco packages.'''.strip()
        
        part2 = '''
Develop Options:
  packages              Packages to put into development mode. Available choices: all, cisco-
                        distutils, genie, genie.libs, genie.libs.clean, genie.libs.conf,
                        genie.libs.filetransferutils, genie.libs.health, genie.libs.ops,
                        genie.libs.robot, genie.libs.sdk, genie.libs.parser, genie.telemetry,
                        genie.trafficgen, pyats, pyats.contrib, rest.connector, unicon,
                        unicon.plugins, yang.connector
  -e, --external        Clone external public repositories instead of internal. Only applicable to
                        internal Cisco pyATS installations. For external pyATS Installations,
                        external public repositories will always be used (Optional)
  -d, --directory DIRECTORY
                        Absolute or relative path of directory to clone repositories into. If not
                        supplied, then the default directory is $VIRTUAL_ENV/pypi (Optional)
  -f, --force-develop   Run 'make develop' even if packages are already in development mode
                        (Optional)
  -s, --skip-version-check
                        Do not check if pyATS packages are up to date before tool execution.
                        WARNING: Using this option may lead to pyATS package version conflicts which
                        could result in a corrupted pyATS installation! Use with discretion
                        (Optional)
  --delete-repos        Delete existing repositories within directory before cloning new ones
                        (Optional) IMPORTANT: Please back up your work before using this option!
  -c, --clone-only      Clone the repositories, but do not put any packages into development mode
                        (Optional)'''.strip()

        part3 = '''General Options:
  -h, --help            Show help
  -v, --verbose         Give more output, additive up to 3 times.
  -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                        and CRITICAL logging levels'''.strip()

        self.assertTrue(part1 in temp_stdout.getvalue().strip())
        self.assertTrue(part2 in temp_stdout.getvalue().strip())
        self.assertTrue(part3 in temp_stdout.getvalue().strip())


    def test_undevelop_help(self):

        temp_stdout = StringIO()
        with redirect_stdout(temp_stdout):
            try:
                entrypoint_main(['undevelop', '--help'])
            except SystemExit:
                pass

        part1 = '''
Usage:
  pyats undevelop [packages...] [options]
  
Usage Examples:
  pyats undevelop all
  pyats undevelop genie.libs.sdk --skip-version-check
  pyats undevelop genie.libs.parser genie.trafficgen --external
  pyats undevelop genie.libs unicon.plugins

Description:
  Removes listed pyATS packages from development mode. Each listed package is 
  removed from development mode with 'make undevelop' and then is reinstalled 
  using 'pip install <package>'. Internal Cisco packages will be reinstalled if 
  the pyATS installation is internal, otherwise external packages will be 
  reinstalled instead.'''.strip()
        
        part2 = '''
Undevelop Options:
  packages              Packages to remove from development mode. Available choices: all, cisco-
                        distutils, genie, genie.libs, genie.libs.clean, genie.libs.conf,
                        genie.libs.filetransferutils, genie.libs.health, genie.libs.ops,
                        genie.libs.robot, genie.libs.sdk, genie.libs.parser, genie.telemetry,
                        genie.trafficgen, pyats, pyats.contrib, rest.connector, unicon,
                        unicon.plugins, yang.connector
  -s, --skip-version-check
                        Do not check if pyATS packages are up to date before tool execution.
                        WARNING: Using this option may lead to pyATS package version conflicts which
                        could result in a corrupted pyATS installation! Use with discretion
                        (Optional)
  -e, --external        Reinstall external public pip packages instead of internal. Only applicable
                        to internal Cisco pyATS installations. For external pyATS Installations,
                        external public pip packages will always be used (Optional)'''.strip()

        part3 = '''
General Options:
  -h, --help            Show help
  -v, --verbose         Give more output, additive up to 3 times.
  -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                        and CRITICAL logging levels
        '''.strip()

        self.assertTrue(part1 in temp_stdout.getvalue().strip())
        self.assertTrue(part2 in temp_stdout.getvalue().strip()) 
        self.assertTrue(part3 in temp_stdout.getvalue().strip())

    def test_invalid_package_name(self):

        temp_stdout = StringIO()
        temp_stderr = StringIO()
        invalid_name = 'invalidpackagename'

        with self.assertRaises(Exception), \
            redirect_stdout(temp_stdout), redirect_stderr(temp_stderr) as cm1:
            entrypoint_main(['develop', invalid_name, '--skip-version-check'])
            self.assertIn('''CRITICAL:pyats.cli.base:
Package invalidpackagename is not an available choice for the current installation mode. Please choose from one or more of the following options: 

    all
    cisco-distutils
    genie
    genie.libs
    genie.libs.clean
    genie.libs.conf
    genie.libs.filetransferutils
    genie.libs.health
    genie.libs.ops
    genie.libs.robot
    genie.libs.sdk
    genie.libs.parser
    genie.telemetry
    genie.trafficgen
    pyats
    pyats.contrib
    rest.connector
    unicon
    unicon.plugins''', cm1.output)

        with self.assertRaises(Exception), \
            redirect_stdout(temp_stdout), redirect_stderr(temp_stderr) as cm2:
            entrypoint_main(['undevelop', invalid_name, '--skip-version-check'])
            self.assertIn('''CRITICAL:pyats.cli.base:
Package invalidpackagename is not an available choice for the current installation mode. Please choose from one or more of the following options: 

    all
    cisco-distutils
    genie
    genie.libs
    genie.libs.clean
    genie.libs.conf
    genie.libs.filetransferutils
    genie.libs.health
    genie.libs.ops
    genie.libs.robot
    genie.libs.sdk
    genie.libs.parser
    genie.telemetry
    genie.trafficgen
    pyats
    pyats.contrib
    rest.connector
    unicon
    unicon.plugins''', cm2.output)


        with self.assertRaises(Exception), \
            redirect_stdout(temp_stdout), redirect_stderr(temp_stderr) as cm3:
            entrypoint_main(['undevelop', invalid_name, '--skip-version-check', 
                                                        '--external'])
            self.assertIn('''CRITICAL:pyats.cli.base:
Package invalidpackagename is not an available choice for the current installation mode. Please choose from one or more of the following options: 

    all
    genie.libs
    genie.libs.clean
    genie.libs.conf
    genie.libs.filetransferutils
    genie.libs.health
    genie.libs.ops
    genie.libs.robot
    genie.libs.sdk
    genie.libs.parser
    genie.telemetry
    genie.trafficgen
    pyats.contrib
    rest.connector
    unicon.plugins''', cm3.output)

    def test_venv_all_internal_bb(self):
        ''' 
            Build new virtual environment and put all internal packages into and 
            then remove them from development mode. 

            Steps:
            - Create a new virtual environment
            - Install pyATS (internal installation)
            - Put this genie repo into dev mode in the new venv
            - pyats develop all
            - Check correct packages are in dev mode
            - pyats undevelop all
            - Check correct packages are not in dev mode
        '''

        global temp_dir

        log.debug("Building internal blackbox env...")
        venv_path = os.path.join(temp_dir, 'internal_bb')

        # Create the venv
        cmd("%s -m venv %s" % (sys.executable, venv_path))

        binary_dir = os.path.join(venv_path, 'bin')
        pip_binary = os.path.join(binary_dir, 'pip')
        activate_path = os.path.join(binary_dir, 'activate')

        # Install pyats, upgrade pip, install virtualenv-clone
        cmd("%s install --upgrade pip setuptools" % pip_binary)
        cmd('%s install -i https://pyats-pypi.cisco.com/simple '
            'cisco-distutils "ats[full]"' % pip_binary)
        # Put this genie repo into dev mode in test venv
        cmd(". %s && make develop -C %s" % 
            (activate_path, Path(os.path.realpath(__file__)).parents[4]))    

        # List packages to be put into and then removed from dev mode
        installed_packages = [
            'ats', 'ats.aereport', 'ats.aetest', 'ats.async', 'ats.cisco', 
            'ats.connections', 'ats.datastructures', 'ats.easypy','ats.kleenex', 
            'ats.log', 'ats.reporter', 'ats.results', 'ats.robot', 'ats.tcl', 
            'ats.topology', 'ats.utils','cisco-distutils', 'genie', 
            'genie.libs.clean','genie.libs.conf','genie.libs.filetransferutils', 
            'genie.libs.health', 'genie.libs.ops', 'genie.libs.robot', 
            'genie.libs.sdk', 'genie.libs.parser', 'genie.telemetry', 
            'genie.trafficgen', 'pyats.contrib', 'rest.connector', 
            'unicon', 'unicon.plugins']

        temp_stdout = StringIO()
        temp_stderr = StringIO()
        with redirect_stdout(temp_stdout), redirect_stderr(temp_stderr):
            # pyats develop all --skip-version-check and then check packages are 
            # in dev mode
            cmd('. %s && pyats develop all -s' % activate_path)
            self.assert_pkgs_in_dev_mode(installed_packages, pip_binary)

            # pyats undevelop all --skip-version-check and then check packages 
            # are not in dev mode
            # then make sure packages were reinstalled using pip install
            cmd('. %s && pyats undevelop all -s' % activate_path)
            self.assert_pkgs_not_in_dev_mode(installed_packages, pip_binary)
            self.assert_pkgs_installed(installed_packages, pip_binary)


    def test_venv_all_external_bb(self):
        ''' 
            Build new virtual environment and put all external packages into and 
            then remove them from development mode.

            Steps:
            - Create a new virtual environment
            - Install pyATS (external installation)
            - Put this genie repo into dev mode in the new venv
            - pyats develop all
            - Check correct packages are in dev mode
            - pyats undevelop all
            - Check correct packages are not in dev mode
        '''

        global temp_dir

        log.debug("Building external blackbox env...")
        venv_path = os.path.join(temp_dir, 'external_bb')

        # Create the venv
        cmd("%s -m venv %s" % (sys.executable, venv_path))

        binary_dir = os.path.join(venv_path, 'bin')
        pip_binary = os.path.join(binary_dir, 'pip')
        activate_path = os.path.join(binary_dir, 'activate')

        # Install pyats, upgrade pip, install virtualenv-clone
        cmd("%s install --upgrade pip setuptools" % pip_binary)
        cmd('%s install "pyats[full]"' % pip_binary)
        cmd('%s install -i https://pyats-pypi.cisco.com/simple '
            'cisco-distutils genie.libs.cisco' % pip_binary)
        # Put this genie repo into dev mode in test venv
        cmd(". %s && make develop -C %s" % 
            (activate_path, Path(os.path.realpath(__file__)).parents[4]))

        # List packages to be put into and then removed from dev mode
        installed_packages = [
            'genie.libs.clean','genie.libs.conf','genie.libs.filetransferutils', 
            'genie.libs.health', 'genie.libs.ops', 'genie.libs.robot', 
            'genie.libs.sdk', 'genie.libs.parser', 'genie.telemetry', 
            'genie.trafficgen', 'pyats.contrib', 'rest.connector', 
            'unicon.plugins']

        temp_stdout = StringIO()
        temp_stderr = StringIO()
        with redirect_stdout(temp_stdout), redirect_stderr(temp_stderr):
            # pyats develop all --skip-version-check and then check packages are 
            # in dev mode
            self.assert_pkgs_not_in_dev_mode(installed_packages, pip_binary)
            cmd('. %s && pyats develop all -s' % activate_path)
            self.assert_pkgs_in_dev_mode(installed_packages, pip_binary)

            # pyats undevelop all --skip-version-check and then check packages 
            # are not in dev mode
            # then make sure packages were reinstalled using pip install
            cmd('. %s && pyats undevelop all -s' % activate_path)
            self.assert_pkgs_not_in_dev_mode(installed_packages, pip_binary)
            self.assert_pkgs_installed(installed_packages, pip_binary)


if __name__ == '__main__':
    unittest.main()
