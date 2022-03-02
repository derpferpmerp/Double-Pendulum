import json
import os
import subprocess

import ffmpeg
from manim import *


def get_frame_rate(filename):
    if not os.path.exists(filename):
        sys.stderr.write(f"ERROR: filename {filename} was not found!")
        return -1
    out = subprocess.check_output(["ffprobe",filename,"-v","0","-select_streams","v","-print_format","flat","-show_entries","stream=r_frame_rate"]).decode("utf-8")
    rate = out.split('"')[1].split("/")
    if len(rate) == 1:
        return float(rate[0])
    if len(rate) == 2:
        return float(rate[0])/float(rate[1])
    return -1

def smartJoin(items, connection=", "):
    strings = []
    for item in items:
        stringed = ""
        if not isinstance(item, str):
            stringed = str(item)
        strings.append(stringed)
    return f"{connection}".join(strings)

def convertToPairs(inList:list, length=2, exclusive=False):
    if length > len(inList):
        generateArgumentError = "\n".join([
            "The Value of the Argument \"length\" was greater than",
            "The Value of the Input List.",
            "Your Arguments:",
            f"inList: {smartJoin(inList)}",
            f"length: {length}",
        ])
        raise ValueError(generateArgumentError)
    pairs = []
    if exclusive:
        for i in range(len(inList)//length):
            s_index = i * length
            LST_APP = []
            for j in range(length):
                LST_APP.append(inList[j + s_index])
            pairs.append(LST_APP)
    else:
        for i in range(len(inList) - length + 1):
            ll = []
            for x in range(length):
                ll.append(inList[i + x])
            pairs.append(ll)
    return pairs

class MovingDots(Scene):
    def constructLine(self, dots, color=RED):
        if isinstance(color,list):
            if len(color) != len(dots) - 1:
                constructValueError = "\n".join([
                    "The Length of the Argument \"color\" should be",
                    "The same length as the Argument \"dots\".",
                    "Your Arguments:",
                    f"Color:  {smartJoin(color)}",
                    f"Dots: {smartJoin(dots)}",
                ])
                raise ValueError(constructValueError)

        lines = []
        coloredSet = [ color] * ( len(dots) - 1) if not isinstance(color, list) else color
        PAIRS = convertToPairs(dots)
        for dotpair, clr in list(zip(PAIRS, coloredSet)):
            line = Line( dotpair[0].get_center(), dotpair[1].get_center()).set_color(clr)
            line.add_updater(lambda z: z.become(Line( dotpair[0].get_center(), dotpair[1].get_center())))
            lines.append(line)

        return lines

    def constructDotUpdaters(self, mappings):
        for tracker in mappings:
            for dot, xmap, ymap in mappings:
                dot.add_updater(lambda z: z.set_x(xmap.get_value()))
                dot.add_updater(lambda z: z.set_y(ymap.get_value()))

    def convertListtoValueTracker(self, lst:list):
        items = []
        for itm in lst:
            LL = []
            for j in itm:
                LL.append(ValueTracker(j))
            items.append(LL)
        return items

    def parseJsonInput(self, file):
        if not os.path.exists(file):
            raise OSError(f"File {file} does not exist in the current directory")
        with open(file) as infile:
            data = json.load(infile)
        CLR_1 = data["CLR_1"]
        CLR_2 = data["CLR_2"]
        DELAY = data["DELAY"]
        NODE_INIT = data["NODE_INIT"]
        FIRS_INIT = data["FIRS_INIT"]
        SECO_INIT = data["SECO_INIT"]
        COORDINATES = data["COORDINATES"]
        LEN_1 = data["LEN_1"]
        LEN_2 = data["LEN_2"]
        return [CLR_1, CLR_2, DELAY, NODE_INIT, FIRS_INIT, SECO_INIT, COORDINATES, LEN_1, LEN_2]

    def changeVideoSpeed(self, inputFileName, outputFileName="output.mp4", removeOldVideo=True, RATIO=None):
        if RATIO is None:
            RATIO = 2 # Change the Speed of the video ( 2 = Double The Speed )
        FRAME_RATE = get_frame_rate(inputFileName)
        stream = ffmpeg.input(inputFileName)
        stream = ffmpeg.setpts(stream, f"{1/RATIO:.3f}*PTS")
        stream = ffmpeg.output(stream, "test.mp4", r=str(FRAME_RATE*RATIO))
        ffmpeg.run(stream)
        if removeOldVideo: os.remove(inputFileName)

    def construct(self, FILE="tmp.json"):

        if FILE is None:
            CLR_1 = RED # Color From First Dot to Second Node
            CLR_2 = GREEN # Color From Second Dot to Third Node
            DELAY = 1.5 # Second Delay Between Movement of States
            NODE_INIT = [ 0, 0]
            FIRS_INIT = [ 0, -1]
            SECO_INIT = [ 0, -2]

            # Coordinates:
            # [ Node(0) scnd(0) thrd(0) ]
            # [ Node(1) scnd(1) thrd(1) ]
            # [ Node(2) scnd(2) thrd(2) ]
            coordinates = [
                [ [0, 0], [0, 0], [0, 0]],
                [ [0, 0], [1, -1], [0, -2]],
                [ [0, 0], [0, -1], [1, -2]],
                [ [0, 0], [-1, -1], [0, -2]],
            ]
        else:
           CLR_1, CLR_2, DELAY, NODE_INIT, FIRS_INIT, SECO_INIT, coordinates, LEN_1, LEN_2 = self.parseJsonInput(FILE)

        # --------------------------------------------------------
        SHOW_PATH_FIRST = {
            "ENABLED": True,
            "DISSTIME": False,#0.4,
            "OPACITY": [0, 1],
            "COLOR": WHITE,
        }

        SHOW_PATH_BOTTO = {
            "ENABLED": True,
            "DISSTIME": False,#0.4,
            "OPACITY": [0, 1],
            "COLOR": RED,
        }
        # --------------------------------------------------------

        AX_LEN = 1.5 * ( LEN_1 + LEN_2)
        ax = Axes(
            x_range=[-AX_LEN, AX_LEN, 2 * AX_LEN],
            y_range=[-AX_LEN, AX_LEN, 2 * AX_LEN],
            x_length=9,
            y_length=9,
            tips=False,
            axis_config={"color":BLACK},
        )

        d1 = Dot(color=RED) # Root Node
        d2 = Dot(color=GREEN) # Second Node
        d3 = Dot(color=BLUE) # Third Node

        PathGroup = VGroup()

        if SHOW_PATH_FIRST["ENABLED"]:

            dissTime = SHOW_PATH_FIRST["DISSTIME"]
            pathOp1 = dissTime/DELAY if dissTime else None

            firstPath = TracedPath(
                d2.get_center,
                dissipating_time=pathOp1,
                stroke_opacity=SHOW_PATH_FIRST["OPACITY"],
                stroke_color=SHOW_PATH_FIRST["COLOR"],
            )
            PathGroup.add(firstPath)

        if SHOW_PATH_BOTTO["ENABLED"]:

            dissTime = SHOW_PATH_BOTTO["DISSTIME"]
            pathOp2 = dissTime/DELAY if dissTime else None

            secondPath = TracedPath(
                d3.get_center,
                dissipating_time=pathOp2,
                stroke_opacity=SHOW_PATH_BOTTO["OPACITY"],
                stroke_color=SHOW_PATH_BOTTO["COLOR"],
            )
            PathGroup.add(secondPath)



        [ d1, d2, d3]

        dg = VGroup(d1, d2, d3)

        NODE_INIT_X, NODE_INIT_Y, *null = ax.c2p(*NODE_INIT)
        FIRS_INIT_X, FIRS_INIT_Y, *null = ax.c2p(*FIRS_INIT)
        SECO_INIT_X, SECO_INIT_Y, *null = ax.c2p(*SECO_INIT)

        NODE_INIT = [ NODE_INIT_X, NODE_INIT_Y]
        FIRS_INIT = [ FIRS_INIT_X, FIRS_INIT_Y]
        SECO_INIT = [ SECO_INIT_X, SECO_INIT_Y]

        p0_x = ValueTracker(NODE_INIT[0])
        p0_y = ValueTracker(NODE_INIT[1])

        p1_x = ValueTracker(FIRS_INIT[0])
        p1_y = ValueTracker(FIRS_INIT[1])

        p2_x = ValueTracker(SECO_INIT[0])
        p2_y = ValueTracker(SECO_INIT[1])

        d1.add_updater(lambda z: z.set_x(p0_x.get_value()))
        d1.add_updater(lambda z: z.set_y(p0_y.get_value()))

        d2.add_updater(lambda z: z.set_x(p1_x.get_value()))
        d2.add_updater(lambda z: z.set_y(p1_y.get_value()))

        d3.add_updater(lambda z: z.set_x(p2_x.get_value()))
        d3.add_updater(lambda z: z.set_y(p2_y.get_value()))

        line1 = Line( d1.get_center(), d2.get_center()).set_color(CLR_1)
        line2 = Line( d2.get_center(), d3.get_center()).set_color(CLR_2)

        lg = VGroup(line1, line2)

        line1.add_updater(lambda z: z.become(Line( d1.get_center(), d2.get_center())))
        line2.add_updater(lambda z: z.become(Line( d2.get_center(), d3.get_center())))

        self.add(ax, PathGroup, lg, dg)

        for coordinateSystem in coordinates:
            (cd1x, cd1y), (cd2x, cd2y), (cd3x, cd3y) = coordinateSystem
            cd1x, cd1y, *null = ax.c2p(cd1x, cd1y)
            cd2x, cd2y, *null = ax.c2p(cd2x, cd2y)
            cd3x, cd3y, *null = ax.c2p(cd3x, cd3y)
            self.play(
                p0_x.animate.set_value(cd1x),
                p0_y.animate.set_value(cd1y),
                p1_x.animate.set_value(cd2x),
                p1_y.animate.set_value(cd2y),
                p2_x.animate.set_value(cd3x),
                p2_y.animate.set_value(cd3y),
            )
            self.wait(0)
