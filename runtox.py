# -*- coding: utf-8 -*-
import re
import sys
import subprocess


section_re = re.compile(r'\[testenv\:(.*)\]')


def runtox(tox_ini_file_name):
    with open(tox_ini_file_name, 'r') as toxini:
        envs = [
            section_re.findall(line)[0]
            for line in map(str.strip, toxini.readlines())
            if section_re.match(line)
        ]
    cmd = ['tox', '-e', ','.join(envs)]

    print("")
    print("    Running command: %s" % ' '.join(cmd))
    print("")

    subprocess.call(cmd)


if __name__ == '__main__':
    runtox('tox.ini' if len(sys.argv) == 1 else sys.argv[2])
