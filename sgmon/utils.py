import os
import sys


def env_lookup(key, msg=""):
    try:
        value = os.environ[key]
        return value
    except KeyError:
        print("{} not found, exiting...\n".format(msg), file=sys.stderr)
        sys.exit(1)
