import frameClient
import cv2

def process_frame(frame):
    # Example of processing the frame
    # Here we just convert it to grayscale and display it
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Processed Frame (press q to exit)", gray_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise KeyboardInterrupt  # Exit on 'q' press

if __name__ == "__main__":
    frameClient.main(callbackFunc=process_frame)