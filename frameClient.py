import cv2
import mmap
import numpy as np
import os
import time
import sys  # Import sys to use sys.exit()
import cameraServer

FRAME_WIDTH = cameraServer.FRAME_WIDTH
FRAME_HEIGHT = cameraServer.FRAME_HEIGHT
FRAME_SIZE_MULTIPLIER = cameraServer.FRAME_SIZE_MULTIPLIER
FRAME_LOCK_FILE_NAME = cameraServer.FRAME_LOCK_FILE_NAME
FRAME_MMAP_FILE_NAME = cameraServer.FRAME_MMAP_FILE_NAME

def acquire_lock():
    while not os.path.exists(FRAME_LOCK_FILE_NAME):
        time.sleep(0.01)  # Prevent this loop from becoming a CPU hog.

def release_lock():
    if os.path.exists(FRAME_LOCK_FILE_NAME):
        os.unlink(FRAME_LOCK_FILE_NAME)

def check_mmap_file_exists(file_path):
    """Check if the memory-mapped file exists and return a boolean."""
    return os.path.exists(file_path)

def main(callbackFunc=None, windowName="Shared Frame (press q to exit)", showOriginalFrame=False):
    frame_height, frame_width = FRAME_HEIGHT, FRAME_WIDTH
    frame_size = frame_height * frame_width * FRAME_SIZE_MULTIPLIER
    mmap_file_path = f"{FRAME_MMAP_FILE_NAME}"

    mm = None
    if not check_mmap_file_exists(mmap_file_path):
        print(f"Error: The file {mmap_file_path} does not exist. Please ensure the server is running.")
        sys.exit(1)  # Exit the script since the mmap file is essential

    print("Frame client started. Press CTRL+C to exit.")
    try:
        with open(mmap_file_path, "r+b") as f:
            mm = mmap.mmap(f.fileno(), frame_size)
            while True:
                acquire_lock()
                mm.seek(0)
                frame_data = mm.read(frame_size)
                release_lock()

                frame = np.frombuffer(frame_data, dtype=np.uint8).copy().reshape((FRAME_HEIGHT, FRAME_WIDTH, FRAME_SIZE_MULTIPLIER))

                if callbackFunc:
                    callbackFunc(frame)

                if showOriginalFrame:
                    cv2.imshow(windowName, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except KeyboardInterrupt:
        print("Termination requested by user.")
    finally:
        if mm:
            mm.close()  # Close the memory-mapped file
        cv2.destroyAllWindows()  # Close all OpenCV windows
        release_lock()  # Ensure the lock file is cleaned up on exit
        print("Finished.")

if __name__ == "__main__":
    main(showOriginalFrame=True)
