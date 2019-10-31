#-*- coding: utf-8 -*-
import logging
import argparse
import subprocess
import configparser
from setuptools import setup

log = logging.getLogger("qi.dist")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

class Installer:
    def __init__(self, args):
        self.args = args
        config = configparser.ConfigParser()
        config.read('conf.ini')
        self.version = config["qi"]["version"]

    def setup(self):
        output = subprocess.check_output(["python", "setup.py", "bdist_wheel"])
        self.log_output(output)

    def install_qi(self):
        output = subprocess.check_output(["pip", "install", f"dist/qi-{self.version}-py3-none-any.whl"])
        self.log_output(output)

    def uninstall_qi(self):
        output = subprocess.check_output(["pip", "uninstall", "-y", "qi"])
        self.log_output(output)

    def log_output(self, output):
        if self.args.verbose:
            log.info(output)

def main():
    log.info("install qi main")
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="output verbosity", action="store_true")
    args = parser.parse_args()

    installer = Installer(args)
    installer.setup()
    installer.uninstall_qi()
    installer.install_qi()

if __name__ == "__main__":
    main()