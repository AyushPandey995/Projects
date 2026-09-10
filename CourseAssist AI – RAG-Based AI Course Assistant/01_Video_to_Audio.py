import os
import subprocess

files = os.listdir("videos")
print(files)

for file in files:
    # print(file)
    tutorial_no = file.split("#")[1].split("_")[0]
    tutorial_name = file.split("_")[1].split("-")[0]
    print(tutorial_no, tutorial_name)
    """How to use ffmpeg - 
    ffmpeg [input options] -i input_file [output options] output_file
    Example - ffmpeg -i input.mp4 -vn -c:a libmp3lame -q:a 2 output.mp3"""
    subprocess.run([
    "ffmpeg",
    "-i",
    f"videos/{file}",
    f"audios/{tutorial_no}_{tutorial_name}.mp3"
    ])

