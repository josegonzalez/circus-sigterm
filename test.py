#!/usr/bin/env python

import time
import signal
import sys


def sighandler(signum, frame):
    print('Received {0}'.format(signum))
    sys.exit(0)


def setup_handlers():
    for i in [x for x in dir(signal) if x.startswith('SIG')]:
        try:
            signum = getattr(signal, i)
            signal.signal(signum, sighandler)
        except (RuntimeError, ValueError), e:
            print 'Skipping {0} due to {1}'.format(i, e)


def main():
    setup_handlers()
    while True:
        print('sleeping')
        time.sleep(1)


if __name__ == "__main__":
    main()
