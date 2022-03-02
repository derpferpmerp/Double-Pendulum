import json
import os
import sys

from numpy import pi as PI

from pend import Pendulum


def safeRemove(filename):
    if os.path.exists(filename):
        os.remove(filename)

def dumpToJson(CLR_1="#FC6255", CLR_2="#83C167"):
    ntheta = -7/8
    ntheta *= PI
    pend = Pendulum(
        THETA_2=2,
        MASS_2=1,
        LEN_2=2.8,
        LEN_1=4,
        MASS_1=1,
        THETA_1=ntheta,
    )
    coords, DELAY, NODE_INIT, FIRS_INIT, SECO_INIT, LEN_1, LEN_2 = pend.generate(
        tmax=5,
        dt=0.02,
    )
    JSON = {
        "CLR_1": CLR_1,
        "CLR_2": CLR_2,
        "DELAY": DELAY,
        "NODE_INIT": NODE_INIT,
        "FIRS_INIT": FIRS_INIT,
        "SECO_INIT": SECO_INIT,
        "COORDINATES": coords,
        "LEN_1": LEN_1,
        "LEN_2": LEN_2,
    }

    def prettyJson(data):
        return json.dumps(data, indent=4)

    safeRemove("tmp.json")
    safeRemove("generator.py")

    with open("tmp.json", "x+") as jsonout:
        jsonout.write(prettyJson(JSON))
    if "@@@" not in sys.argv:
        print(f"Run manim.exe render {os.path.join('.','main.py')} (Runs from json file tmp.json)")


dumpToJson()
