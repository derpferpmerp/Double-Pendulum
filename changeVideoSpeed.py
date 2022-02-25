import ffmpeg, os, subprocess, re, json

def get_frame_rate(filename):
    if not os.path.exists(filename):
        sys.stderr.write(f"ERROR: filename {filename} was not found!")
        return -1
    out = subprocess.check_output(["ffprobe",filename,"-v","0","-select_streams","v","-print_format","flat","-show_entries","stream=r_frame_rate"]).decode("utf-8")
    rate = out.split('"')[1].split('/')
    if len(rate) == 1:
        return float(rate[0])
    if len(rate) == 2:
        return float(rate[0])/float(rate[1])
    return -1

def safeRemove(filename):
    if os.path.exists(filename):
        os.remove(filename)

def get_duration(filename):
    out = subprocess.check_output(["ffprobe",filename,"-v","0","-select_streams","v","-print_format","flat","-show_entries","format=duration"]).decode("utf-8")
    return float(re.findall('(?<=\").*(?=\")', out)[0])

def changeVideoSpeed(inputFileName, jsonfile="tmp.json", outputFileName="output.mp4", removeOldVideo=True):
        safeRemove("midStep.mp4")
        safeRemove("output.mp4")
        with open(jsonfile, "r") as infile:
            data = json.load(infile)

        deltat = data["DELAY"]
        frames = len(data["COORDINATES"])

        RATIO = deltat * frames
        VID_LEN = get_duration(inputFileName)

        RATIO /= VID_LEN

        print(f"{VID_LEN=}, {RATIO=}")

        FRAME_RATE = get_frame_rate(inputFileName)

        print(f"{FRAME_RATE=}")
        stream = ffmpeg.input(inputFileName)
        stream = ffmpeg.setpts(stream, '{0}*PTS'.format(RATIO))
        stream = ffmpeg.output(stream, outputFileName, r=str(60))
        ffmpeg.run(stream)

        #FR = get_frame_rate("midStep.mp4")

        #stream2 = ffmpeg.input("midStep.mp4")
        #stream2 = ffmpeg.setpts(stream2, '{0}*PTS'.format(1/10))
        #stream2 = ffmpeg.output(stream2, outputFileName)
        #ffmpeg.run(stream2)

        if removeOldVideo:
            os.remove(inputFileName)
       
changeVideoSpeed(os.path.join(*["media", "videos", "main", "1080p30", "MovingDots.mp4"]), removeOldVideo=False)