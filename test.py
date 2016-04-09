#!/usr/bin/env python

import os
import time
import signal
import sys


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def sighandler(signum, frame):
    touch('/vagrant/{0}.pid-{1}'.format(signum, os.getpid()))
    print('[pid:{0}] Received {1}'.format(os.getpid(), signum))
    sys.exit(0)


def setup_handlers():
    pid = os.getpid()
    for i in [x for x in dir(signal) if x.startswith('SIG')]:
        try:
            signum = getattr(signal, i)
            signal.signal(signum, sighandler)
        except (RuntimeError, ValueError), e:
            print '[pid:{0}] Skipping {1} due to {2}'.format(pid, i, e)


def main():
    pid = os.getpid()
    setup_handlers()
    while True:
        print('[pid:{0}] sleeping'.format(pid))
        time.sleep(1)


if __name__ == "__main__":
    main()
