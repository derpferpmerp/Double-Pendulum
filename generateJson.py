import json
import re
from pend import Pendulum
import os
from numpy import pi as PI

def safeRemove(filename):
    if os.path.exists(filename):
        os.remove(filename)

def dumpToJson(CLR_1="#FC6255", CLR_2="#83C167"):
    pend = Pendulum(THETA_2=PI/2, MASS_2=1)
    coords, DELAY, NODE_INIT, FIRS_INIT, SECO_INIT, LEN_1, LEN_2 = pend.generate(tmax=20, dt=0.02)
    JSON = {
        "CLR_1": CLR_1,
        "CLR_2": CLR_2,
        "DELAY": DELAY,
        "NODE_INIT": NODE_INIT,
        "FIRS_INIT": FIRS_INIT,
        "SECO_INIT": SECO_INIT,
        "COORDINATES": coords,
        "LEN_1": LEN_1,
        "LEN_2": LEN_2
    }

    def prettyJson(data):
        return json.dumps(data, indent=4)

    safeRemove("tmp.json")
    safeRemove("generator.py")

    with open("tmp.json", "x+") as jsonout:
        jsonout.write(prettyJson(JSON))

    print("Run manim.exe render .\\main.py (Runs from json file tmp.json)")

    
dumpToJson()


