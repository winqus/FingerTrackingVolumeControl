# camera_server.py
import cv2
import mmap
import numpy as np
import os

VIDEO_CAPTURE_DEVICE_ID = 0
FRAME_HEIGHT = 720
FRAME_WIDTH = 1280
FRAME_SIZE_MULTIPLIER = 3
FRAME_LOCK_FILE_NAME = "frame.lock"
FRAME_MMAP_FILE_NAME = "frame.mmap"

def create_lock():
    with open(FRAME_LOCK_FILE_NAME, "w") as f:
        pass

def acquire_lock():
    while os.path.exists(FRAME_LOCK_FILE_NAME):
        continue

def cleanup(mm, filename):
    mm.close()
    os.unlink(filename)
    if os.path.exists(FRAME_LOCK_FILE_NAME):
        os.unlink(FRAME_LOCK_FILE_NAME)

def release_lock():
    create_lock()

def main():
    print("Initializing VideoCapture...")
    cap = cv2.VideoCapture(VIDEO_CAPTURE_DEVICE_ID)
    cap.set(3, FRAME_WIDTH)
    cap.set(4, FRAME_HEIGHT)
    # Define the frame dimensions and the size for the memory map
    frame_height, frame_width = FRAME_HEIGHT, FRAME_WIDTH
    frame_size = frame_height * frame_width * FRAME_SIZE_MULTIPLIER

    print(f"Initialized. VideoCapture(ID={VIDEO_CAPTURE_DEVICE_ID}) is active. Frame size is {frame_size}. ",
          f"Press CTRL+C to exit.")

    # Create a memory-mapped file
    with open(FRAME_MMAP_FILE_NAME, "wb") as f:
        # Initialize the file size
        f.write(bytearray(frame_size))

    mm = None
    try:
        with open(FRAME_MMAP_FILE_NAME, "r+b") as f:
            mm = mmap.mmap(f.fileno(), frame_size)
            create_lock()
            while True:
                ret, frame = cap.read()
                if ret:
                    frame = cv2.resize(frame, (frame_width, frame_height))
                    acquire_lock()
                    mm.seek(0)
                    mm.write(frame.tobytes())
                    release_lock()
    except KeyboardInterrupt:
        print("Termination requested by user.")
    finally:
        if mm:
            cleanup(mm, FRAME_MMAP_FILE_NAME)
        if cap:
            cap.release()
        print("Finished.")


if __name__ == "__main__":
    main()