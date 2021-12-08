#!/usr/bin/env python3
import requests, sys, os, time, traceback, logging
from login import headers

nameCSV = "/json"
termId = 1038

def digdown(stuNum, sessionLogin):
    logger = logging.getLogger(__name__)
    endPro = nameCSV + "/" + str(stuNum) + ".json"
    time.sleep(.35)
    urlL = "https://my.cqu.edu.cn/api/timetable/class/timetable/student/table-detail?sessionId=" + str(termId)
    ret = 0
    while not ret:
        try:
            ret = sessionLogin.post(urlL,
                headers = headers,
                json = [stuNum]
            )
            print(urlL, ret.request.body)
        except Exception as e:
            traceback.print_exc()
            logger.error("[digdown] buggy")
            break
        if ret.status_code != 200:
            logger.debug(ret.content)
            logger.error("[digdown] wrong_status_code")
            break
        elif "classTimetableVOList" not in ret.json():
            logger.error(ret.content)
            logger.error("[digdown] wrong_ret_json")
            break
        with open("." + endPro, "wb") as fileIO:
            fileIO.write(ret.content)
        logger.debug("done " + str(stuNum))
        return ret.content
    return None

# for i in range(20200001, 20206471 + 1):
# for i in range(20190001, 20196341 + 1):
# for i in range(20180001, 20186485 + 1):
# for i in range(20170001, 20176442 + 1):
# digdown()
