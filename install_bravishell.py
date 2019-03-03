#!/usr/bin/env python2
from __future__ import print_function
import subprocess
import argparse
import sys
import os
from urlparse import urljoin
import shlex
import platform
from collections import OrderedDict
if sys.version_info < (3,):
    input = raw_input

"""total 48
drwxrwxrwx  12 psychtests  wheel    408 Feb 20 00:12 .
drwxr-xr-x  36 root        wheel   1292 May 31  2017 ..
-rw-r--r--@  1 psychtests  wheel  14340 Dec  4 12:54 .DS_Store
drwxr-xr-x  12 psychtests  wheel    408 Mar  2 14:24 .git
drwxr-xr-x  45 psychtests  staff   1530 Feb 19 23:42 BraviTests
drwxr-xr-x   6 psychtests  staff    204 Dec  4 12:53 BraviToolbox Archive
drwxr-xr-x  16 psychtests  staff    544 Apr  3  2018 Calibration Files
drwxr-xr-x   9 psychtests  wheel    306 Sep 14 14:38 OLD VERSIONS
drwxr-xr-x   9 psychtests  wheel    306 May 21  2018 PathSettings
drwxr-xr-x   7 psychtests  staff    238 Apr  3  2018 Psychtoolbox Archive
-rwxr-xr-x   1 psychtests  wheel    526 Sep 20  2016 SetupPath.m
-rwxr-xr-x   1 psychtests  wheel      9 Sep 20  2016 startup.m
"""

bravi_gh = r"https://github.com/BraviShell/"
repo_dict = OrderedDict([(urljoin(bravi_gh, "BraviShell"), ""),
                         (urljoin(bravi_gh, "Compiled"), "Compiled"),
                         (urljoin(bravi_gh, "ParameterFiles"), "Parameter Files"),
                         (urljoin(bravi_gh, "Documentation"), "Documentation"),
                         (urljoin(bravi_gh, "PsychToolbox"), "Psychtoolbox Archive"),
                         (urljoin(bravi_gh, "PathSettings"), "PathSettings"),
                         (urljoin(bravi_gh, "CalibrationFiles"), "Calibration Files"),
                         (urljoin(bravi_gh, "BraviToolbox"), "BraviToolbox Archive"),
                         (urljoin(bravi_gh, "BraviTests"), "BraviTests")])


def main(root_dir):
    check_versions()
    root_dir = os.path.abspath(root_dir)
    if not os.path.isdir(root_dir):
        sys.exit('{} is not a directory, aborting!'.format(root_dir))
    print("Cloning repositories.  Please enter your github credentials when prompted if you don't have them cached.")
    for url_key, dest_val in repo_dict.iteritems():
        destination = os.path.join(root_dir, dest_val)
        print('cloning {} to {}'.format(url_key, destination))
        subprocess.check_call(shlex.split('git clone {} "{}"'.format(url_key, destination)))
    print("Finished cloning repositories.")

    print("Setting symbolic link")
    subprocess.check_call(shlex.split('sudo ln -s {} /MatlabTests'.format(root_dir)))
    print("Symbolic link set.")


def check_versions():
    if not is_mac_ok():
        result = input('This operating system has not been tested; continue? [y/N]: ')
        if result.lower() == 'n':
            sys.exit("Exiting; no action taken.")


def is_mac_ok():
    snow_leopard = (10, 6)
    high_sierra = (10, 13)
    try:
        curr_version = tuple(int(x) for x in platform.mac_ver()[0].split('.'))
    except ValueError:
        curr_version = tuple()
    return snow_leopard <= curr_version <= high_sierra



if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("""Usage: install.py ROOT_DIR""")
