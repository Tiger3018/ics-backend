# Oct 13th, 2021 by Tiger3018
# from time import sleep
from cqu_timetable_new import load_from_json, mkical
import datetime, os, traceback, logging

# local import
from login_oauth import login, loginOauth
from get_json import digdown, nameCSV

stuListGlobal = []
prefixStr = _ if (_ := os.getenv("APP_DIR")) else "."

def atOncePassword(stuList) -> None:
    os.makedirs(prefixStr + nameCSV, exist_ok = True)
    os.makedirs(prefixStr + "/ics", exist_ok = True)
    # logging.basicConfig(level="DEBUG")
    with open(prefixStr + "/credentials/password", "r") as fileIO:
        sessionGet = login(fileIO.readline().split()[0], fileIO.readline().split()[0])
        if not sessionGet:
            raise Exception("session get error")
        # else:
            # logging.getLogger(__name__).debug(sessionGet.headers)
        # sleep(2)
        for i in stuList:
            try:
                jsonStr = digdown(i, sessionGet)
                rawData = load_from_json(jsonStr)
                rawIcal = mkical(rawData, datetime.date(2022, 2, 14), 0)
                with open(prefixStr + "/ics/" + str(i) + ".ics", "wb") as outputIO:
                    outputIO.write(rawIcal.to_ical())
            except Exception as e :
                traceback.print_exc()

def atOnceOauthSession(stuNum : str) -> None:
    oauth_tgt = None
    try:
        with open(prefixStr + "/credentials/oauth", "r") as fileIO:
            oauth_tgt = fileIO.readline().split()[0]
    except Exception:
        pass
    finally:
        if not oauth_tgt:
            oauth_tgt = os.getenv("OAUTH_TGT")
    sessionGet = loginOauth(oauth_tgt)
    if not sessionGet:
        raise Exception("session get error")
    try:
        jsonStr = digdown(stuNum, sessionGet)
        if rawData := load_from_json(jsonStr): # no class info
            rawIcal = mkical(rawData, datetime.date(2022, 2, 14), 0)
            with open(prefixStr + "/ics/" + stuNum + ".ics", "wb") as outputIO:
                outputIO.write(rawIcal.to_ical())
        else:
            return
    except Exception:
        traceback.print_exc()
