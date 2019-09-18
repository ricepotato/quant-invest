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
bld_path = os.path.join(cur_path, "build")

class WorkingDir:
    def __init__(self, path):
        self.cwd = path
        self.owd = None

    def __enter__(self):
        self.owd = os.getcwd()
        os.chdir(self.cwd)

    def __exit__(self, e_type, e_value, tb):
        os.chdir(self.cwd)

    def cwd(self):
        return self.cwd

    def owd(self):
        return self.owd


class Builder:
    def __init__(self):
        self.cur_path = os.path.dirname(__file__)
        self.main_path = os.path.join(self.cur_path, "src", "main")
        self.bld_path = os.path.join(cur_path, "build")
        self.srv_bld_path = os.path.join(self.bld_path, "server")
        self.build_action = {
            "server":self._build_server
        }

    def build(self, target):
        log.info("build start target=%s", target)
        return self.build_action.get(target)()

    def _build_server(self):
        log.info("build server...")
        res = self._compress("common")
        res = self._compress("data")
        res = self._compress("server")

        mod_gzs = map(lambda module: self._compress(module), 
                      ["common", "data", "server"])

        for filepath in mod_gzs:
            self._move_to(filepath, self.srv_bld_path)

    def _compress(self, package):
        with WorkingDir(self.main_path) as wd:
            gz_filepath = os.path.join(self.main_path, f"{package}.tar.gz")
            if os.path.exists(gz_filepath):
                os.remove(gz_filepath)
            res = subprocess.check_output(["tar", "-cvf", f"{package}.tar", f"./{package}"])
            log.debug(res)
            res = subprocess.check_output(["gzip", "-v", f"./{package}.tar"])
            log.debug(res)
            log.info("compressed:%s", gz_filepath)
            return gz_filepath

    def _move_to(self, filepath, dest_path):
        filename = os.path.split(filepath)[-1]
        dest_filepath = os.path.join(dest_path, filename)
        log.info("gz file move %s -> %s", filepath, dest_filepath)
        os.rename(filepath, dest_filepath)
        return dest_filepath

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