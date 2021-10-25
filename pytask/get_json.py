#!/usr/bin/env python3
import requests, sys, os, time, traceback, logging
from login import headers

nameCSV = "/json"

def digdown(stuNum, sessionLogin):
    logger = logging.getLogger(__name__)
    endPro = nameCSV + "/" + str(stuNum) + ".json"
    time.sleep(.35)
    urlL = "http://my.cqu.edu.cn/api/enrollment/timetable/student/" + str(stuNum)
    ret = 0
    while not ret:
        try:
            print(urlL)
            ret = sessionLogin.get(urlL, headers = headers)
        except Exception as e:
            traceback.print_exc()
            logger.error("<!>buggy")
            break
        if ret.status_code != 200:
            logger.debug(ret.content)
            ret = 0
            logger.error("<!>wrong_status_code")
            break
        with open("." + endPro, "wb") as fileIO:
            fileIO.write(ret.content)
        logger.debug("done " + str(stuNum))
        return ret.content

# for i in range(20200001, 20206471 + 1):
# for i in range(20190001, 20196341 + 1):
# for i in range(20180001, 20186485 + 1):
# for i in range(20170001, 20176442 + 1):
# digdown()