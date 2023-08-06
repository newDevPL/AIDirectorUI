import os
import subprocess

# Folder containing video and audio files
folder_path = "./output"

# Get list of files in the directory
files = os.listdir(folder_path)

# Sort the files to ensure they're concatenated in the correct order
files.sort()

# Split into video and audio files
video_files = [f for f in files if f.endswith(('.mp4', '.flv', '.mov'))]  # add more video formats as needed
audio_files = [f for f in files if f.endswith(('.mp3', '.wav', '.flac', '.m4a'))]  # add more audio formats as needed

# Create a temporary file with the names of all videos to be concatenated
with open("concat.txt", "w") as f:
    for video_file in video_files:
        f.write("file '" + os.path.join(folder_path, video_file) + "'\n")

if audio_files:
    # Assuming there is only one audio file in the directory
    audio_file = os.path.join(folder_path, audio_files[0])

    # Concatenate all videos and add the audio track
    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "concat.txt",
        "-i", audio_file,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "output_temp.mp4"
    ])
else:
    # Concatenate all videos without adding any audio track
    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "concat.txt",
        "-c:v", "copy",
        "output_temp.mp4"
    ])

# Get a unique name for the final output file
counter = 1
output_filename = "final_output.mp4"
while os.path.exists(output_filename):
    output_filename = f"final_output_{counter}.mp4"
    counter += 1

# Convert the output to x265
subprocess.run([
    "ffmpeg",
    "-i", "output_temp.mp4",
    "-c:v", "libx265",
    "-crf", "23",  # Constant Rate Factor (CRF). Lower number is higher quality. Typically 18-28 is acceptable. For high quality try a lower number like 18-20.
    "-c:a", "aac",  # using the aac codec for audio
    "-b:a", "384k",  # Audio bitrate. You may adjust as necessary.
    output_filename
])

# Remove temporary files
os.remove("concat.txt")
os.remove("output_temp.mp4")

print("Video successfully created!")
