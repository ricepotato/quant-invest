#-*- coding: utf-8 -*-

import os
import argparse
import subprocess
import logging

log = logging.getLogger("qi.build")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

cur_path = os.path.dirname(__file__)
main_path = os.path.join(cur_path, "src", "main")

def compress(package):
    res = subprocess.check_output(["tar", "-cvf", f"{package}.tar", f"./{package}"])
    log.debug(res)
    res = subprocess.check_output(["gzip", "-v", f"./{package}.tar"])
    log.debug(res)

def build_server():
    
    oldpath = os.getcwd()
    os.chdir(main_path)

    res = subprocess.check_output(["tar", "-cvf", "common.tar", "./common"])
    log.debug(res)
    res = subprocess.check_output(["gzip", "-v", "./common.tar"])
    log.debug(res)

    return 0

class Builder:
    def __init__(self):
        self.cur_path = os.path.dirname(__file__)
        self.main_path = os.path.join(self.cur_path, "src", "main")
        self.build_action = {
            "server":self._build_server
        }

    def build(self, target):
        log.info("build start target=%s", target)
        return self.build_action.get(target)()

    def _build_server(self):
        log.info("build server...")
        self._compress("common")
        self._compress("data")
        self._compress("server")
       

    def _compress(self, package):
        oldpath = os.getcwd()
        os.chdir(self.main_path)
        res = subprocess.check_output(["tar", "-cvf", f"{package}.tar", f"./{package}"])
        log.debug(res)
        res = subprocess.check_output(["gzip", "-v", f"./{package}.tar"])
        log.debug(res)

        os.chdir(oldpath)

def main():
    log.info("build.py run")
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default=None, help="specify target.", required=True)
    args = parser.parse_args()

    builder = Builder()
    res = builder.build(args.target)
    log.info("build complete %s", str(res))

if __name__ == "__main__":
    main()