import cv2
import numpy as np
import time
import os
from rich.console import Console

# Setup
ASCII_CHARS = "@%#*+=-:. "  # from darkest to brightest
console = Console()
WIDTH = 120  # Width of ASCII output
FPS = 15     # Frames per second for playback

def frame_to_ascii(frame, width):
    height, original_width = frame.shape
    aspect_ratio = original_width / height
    new_height = int(width / aspect_ratio / 2)  # aspect correction
    resized = cv2.resize(frame, (width, new_height))
    
    ascii_image = ""
    for row in resized:
        for pixel in row:
            ascii_image += ASCII_CHARS[pixel // 25]
        ascii_image += "\n"
    return ascii_image

def play_video_ascii(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        console.print("[bold red]Error opening video file[/]")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ascii_frame = frame_to_ascii(gray, WIDTH)

        console.clear()
        console.print(f"[bold cyan]{ascii_frame}[/]")
        time.sleep(1 / FPS)

    cap.release()
    console.print("[bold green]Video playback finished. Geronimo![/]")

# Usage
if __name__ == "__main__":
    play_video_ascii("path_to_your_video.mp4")  # Replace with your video file path
