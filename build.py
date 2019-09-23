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
        log.debug("__enter__ self.owd=%s", self.owd)
        os.chdir(self.cwd)

    def __exit__(self, e_type, e_value, tb):
        log.debug("__exit__ self.owd=%s", self.owd)
        os.chdir(self.owd)

    def cwd(self):
        return self.cwd

    def owd(self):
        return self.owd

class AppBuilder:
    def __init__(self, cur_path):
        self.main_path = os.path.join(cur_path, "src", "main")
        self.bld_path = os.path.join(cur_path, "build")

    def _move_to(self, filepath, dest_path):
        filename = os.path.split(filepath)[-1]
        dest_filepath = os.path.join(dest_path, filename)
        log.info("gz file move %s -> %s", filepath, dest_filepath)
        if os.path.exists(dest_filepath):
            os.remove(dest_filepath)
        os.rename(filepath, dest_filepath)
        return dest_filepath

    def _compress(self, package):
        with WorkingDir(self.main_path) as wd:
            gz_filepath = os.path.join(self.main_path, f"{package}.tar.gz")
            log.debug("gz_filepath=%s", gz_filepath)
            if os.path.exists(gz_filepath):
                os.remove(gz_filepath)
            res = subprocess.check_output(["tar", "-cvf", f"{package}.tar", f"./{package}"])
            log.debug(res)
            res = subprocess.check_output(["gzip", "-v", f"./{package}.tar"])
            log.debug(res)
            log.info("compressed:%s", gz_filepath)
            return gz_filepath

    def _run_build(self):
        if self.full:
            with WorkingDir(self.bld_base_path) as wd:
                log.info("build image... base")
                res = subprocess.check_output(["./build.sh"])
                log.info("build image... complete")
                log.debug(res)

        with WorkingDir(self.bld_main_path) as wd:
            log.info("build image... main")
            res = subprocess.check_output(["./build.sh"])
            log.debug(res)
            log.info("build image... complete")

class WebBuilder(AppBuilder):
    def __init__(self, cur_path):
        AppBuilder.__init__(self, cur_path)
        self.full = False
        self.bld_base_path = os.path.join(self.bld_path, "web", "base")
        self.bld_main_path = os.path.join(self.bld_path, "web", "main")
        self.packages = ["web"]

    def run(self, full):
        self.full = full
        log.info("build web.")
        mod_gzs = map(lambda module: self._compress(module), 
                      self.packages)
        for filepath in mod_gzs:
            self._move_to(filepath, self.bld_main_path)
        self._run_build()

class ServerBuilder(AppBuilder):
    def __init__(self, cur_path):
        AppBuilder.__init__(self, cur_path)
        self.full = False
        self.bld_base_path = os.path.join(self.bld_path, "server", "base")
        self.bld_main_path = os.path.join(self.bld_path, "server", "main")
        self.packages = ["common", "data", "server"]

    def run(self, full):
        self.full = full
        log.info("build server.")
        mod_gzs = map(lambda module: self._compress(module), 
                      self.packages)
        for filepath in mod_gzs:
            self._move_to(filepath, self.bld_main_path)
        self._run_build()

class Builder:
    def __init__(self):
        self.cur_path = os.path.abspath(os.path.dirname(__file__))
        self.build_action = {
            "server":ServerBuilder,
            "web":WebBuilder
        }

    def build(self, target, full):
        log.info("build start target=%s", target)
        self.full = full
        self.target = target
        builder = self.build_action.get(target)(self.cur_path)
        return builder.run(self.full)


def main():
    log.info("build.py run")
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default=None, help="specify target.", required=True)
    parser.add_argument("--full", action="store_true", help="specify run full build", required=False)
    parser.add_argument("--debug", action="store_true", help="specify run debug mode", required=False)
    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    builder = Builder()
    res = builder.build(args.target, args.full)
    log.info("build complete %s", str(res))

if __name__ == "__main__":
    main()