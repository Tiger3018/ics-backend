#!/usr/bin/env python3
# Oct 13th, 2021 by Tiger3018
# from time import sleep
from cqu_timetable_new import load_from_json, mkical
import datetime, os, traceback, logging

# local import
from login import login
from get_json import digdown, nameCSV

stuList = []
prefixStr = "./"


def atOnce() -> None:
    os.makedirs(prefixStr + nameCSV, exist_ok = True)
    os.makedirs(prefixStr + "ics", exist_ok = True)
    logging.basicConfig(level="DEBUG")
    with open(prefixStr + "credentials/oauth", "r") as fileIO:
        sessionGet = login(fileIO.readline(), fileIO.readline())
        if not sessionGet:
            raise Exception("session get error")
        # else:
            # logging.getLogger(__name__).debug(sessionGet.headers)
        # sleep(2)
        for i in stuList:
            try:
                jsonStr = digdown(i, sessionGet)
                rawData = load_from_json(jsonStr)
                rawIcal = mkical(rawData, datetime.date(2021, 8, 30), 0)
                with open(prefixStr + "ics/" + str(i) + ".ics", "wb") as outputIO:
                    outputIO.write(rawIcal.to_ical())
            except Exception as e :
                traceback.print_exc()


if __name__ == "__main__":
    atOnce()