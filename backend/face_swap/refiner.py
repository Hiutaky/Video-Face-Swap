import cv2
import os
from moviepy.editor import VideoFileClip

#generate a pre-swap preview video
def generate_video_preview(video_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with VideoFileClip(video_path) as video:
        preview_duration = min(7, video.duration)
        preview_video_path = os.path.join(output_dir, 'preview_input.mp4')
        preview_clip = video.subclip(0, preview_duration)
        preview_clip.write_videofile(preview_video_path, codec = 'libx264', fps=video.fps) 

def generate_preview_and_gif(video_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with VideoFileClip(video_path) as video:
        fps = video.fps
        duration = video.duration
        preview_duration = min(15, duration)
        preview_video_path = os.path.join(output_dir, 'preview.mp4')
        preview_clip = video.subclip(0, preview_duration)
        preview_clip.write_videofile(preview_video_path, codec='libx264', fps=fps)

    gif_duration = min(5, preview_duration)
    gif_path = os.path.join(output_dir, 'preview.gif')
    with VideoFileClip(preview_video_path) as video:
        video.subclip(0, gif_duration).resize((600, 338)).write_gif(gif_path, fps=24, program="ffmpeg")

