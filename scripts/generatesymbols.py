#!/usr/bin/python

import os.path
import subprocess

with open(os.path.join(os.path.dirname(__file__), 'symbols_ssl.txt'), 'w') as f:
    f.writelines(sorted([
        line.split()[2].split('@')[0] + '\n' for line in subprocess.check_output(['nm', '-D', '/usr/lib/x86_64-linux-gnu/libssl.so.3']).decode('utf-8').split('\n') if ' T ' in line
    ]))

with open(os.path.join(os.path.dirname(__file__), 'symbols_crypto.txt'), 'w') as f:
    f.writelines(sorted([
        line.split()[2].split('@')[0] + '\n' for line in subprocess.check_output(['nm', '-D', '/usr/lib/x86_64-linux-gnu/libcrypto.so.3']).decode('utf-8').split('\n') if ' T ' in line
    ]))
