"""Encode actual recorded gameplay with its recorded in-game audio, then append controls."""
import json,subprocess
from pathlib import Path
O=Path("generated-artifacts/mission-forge-package")
def probe(p):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(p)]))
def run(args):
    with (O/"encoding.log").open("a") as log:
        subprocess.run(["ffmpeg","-y","-hide_banner",*map(str,args)],stdout=log,stderr=log,check=True)
main=float(probe(O/"gameplay-raw.webm")["format"]["duration"])
run(["-i",O/"game-audio.webm","-vn","-c:a","pcm_s16le",O/"game-audio.wav"])
audio=float(probe(O/"game-audio.wav")["format"]["duration"])
extra=float(probe(O/"controls.webm")["format"]["duration"])
delay=max(0,round((main-audio)*1000))
run(["-i",O/"gameplay-raw.webm","-i",O/"game-audio.wav","-map","0:v","-map","1:a",
     "-af",f"adelay={delay}:all=1,apad","-t",main,"-r","25","-c:v","libx264","-preset","veryfast","-crf","22",
     "-pix_fmt","yuv420p","-c:a","aac","-ar","48000","-ac","2","-b:a","128k",O/"main.mp4"])
run(["-i",O/"controls.webm","-f","lavfi","-i","anullsrc=r=48000:cl=stereo",
     "-map","0:v","-map","1:a","-t",extra,"-r","25","-c:v","libx264","-preset","veryfast","-crf","22",
     "-pix_fmt","yuv420p","-c:a","aac","-ar","48000","-ac","2","-b:a","128k",O/"controls.mp4"])
(O/"concat.txt").write_text("file 'main.mp4'\nfile 'controls.mp4'\n")
run(["-f","concat","-safe","0","-i",O/"concat.txt","-c","copy","-movflags","+faststart",O/"Mission_Forge_Complete_Demo.mp4"])
info=probe(O/"Mission_Forge_Complete_Demo.mp4")
(O/"video-info.json").write_text(json.dumps(info,indent=2))
print("Video completed:",info["format"]["duration"],"seconds;",info["format"]["size"],"bytes")
