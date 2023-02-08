import os
import random

'''
该代码需要FFmpeg库的支持，请确保已经在系统中安装了FFmpeg。
'''
video_folder = '/path/to/videos'
output_folder = '/path/to/output'
output_file = 'new_video.mp4'

total_size = 0
selected_videos = []

for filename in os.listdir(video_folder):
    file_path = os.path.join(video_folder, filename)
    if os.path.isfile(file_path):
        file_size = os.path.getsize(file_path)
        if total_size + file_size <= 20 * 1024**3:
            selected_videos.append(file_path)
            total_size += file_size
        elif random.random() < (20 * 1024**3 - total_size) / file_size:
            selected_videos = [file_path]
            total_size = file_size

if selected_videos:
    output_path = os.path.join(output_folder, output_file)
    concat_command = 'ffmpeg -i "concat:{}" -c copy "{}"'.format("|".join(selected_videos), output_path)
    os.system(concat_command)

