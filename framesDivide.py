import cv2
import os
import random
import uuid
import tkinter as tk
from tkinter import filedialog

def select_video_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select Input Video",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
    )

def extract_random_frames(video_path, num_frames=15, output_folder="./datasets/masked"):
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Load video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames < num_frames:
        print(f"Video has only {total_frames} frames. Reducing number of outputs.")
        num_frames = total_frames

    # Generate a short UUID for file prefix
    video_id = str(uuid.uuid4().hex)[:8]

    # Select random frame indices
    selected_frames = sorted(random.sample(range(total_frames), num_frames))
    print(f"Extracting frames at indices: {selected_frames}")

    frame_idx = 0
    save_idx = 1

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx in selected_frames:
            filename = os.path.join(output_folder, f"{video_id}_{save_idx}.png")
            cv2.imwrite(filename, frame)
            print(f"Saved: {filename}")
            save_idx += 1

        frame_idx += 1
        if save_idx > num_frames:
            break

    cap.release()
    print("Done.")

# Entry point
if __name__ == "__main__":
    video_path = select_video_file()
    if video_path:
        extract_random_frames(video_path)
    else:
        print("No video selected.")
