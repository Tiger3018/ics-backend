#!/usr/bin/env python3
# Oct 25th, 2021 by Tiger3018

# local import
from base import atOncePassword

if __name__ == "__main__":
    stuListGlobal = [i for i in range(20210001, 20216482 + 1)] + [i for i in range(20200001, 20206471 + 1)]
    atOncePassword(stuListGlobal)