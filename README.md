# Finger Tracking Volume Control

Minimal collection of demos that control system volume using finger tracking (OpenCV + MediaPipe).

## Quick start

1. Create and activate a Python virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

If `pip install -r requirements.txt` fails on the `mediapipe` package (common on macOS/ARM):
- Ensure you are using Python 3.10 (mediapipe may not support later versions well).
```bash
brew install python@3.10
brew link python@3.10
python3.10 -m venv mpenv
source mpenv/bin/activate
pip install --upgrade pip
pip install mediapipe
```


3. Recommended: use the launcher `main.py` from the repository root. It will try to import the target script and call its `main()` when available (preferred), otherwise it will spawn a subprocess.

```bash
python main.py        # interactive menu (default runs v2)
python main.py --list # list options
python main.py v2     # run the v2 demo
```

4. Or run a specific script directly:

```bash
python handTrackingVolumeAdjustV2.py
python handTrackingVolumeAdjust.py
python handTrackingBasic.py
```

## Notes
- The hand detection utilities are in `handTrackingModule.py`.
- Frame sharing server/client: `cameraServer.py` (server) and `frameClient.py` (client).
- `handTrackingVolumeAdjustV2.py` now exposes a `main(showOriginalFrame=False)` function so it can be imported and run by `main.py` without spawning a subprocess.
- The project historically used `pycaw`/`comtypes` which are Windows-specific for audio control. On macOS you may need to replace the volume-control bits (e.g., use `osascript` or `pyobjc` approaches). See `handTrackingVolumeAdjustV2.py` for where audio is set.

Degraded mode
-------------
If MediaPipe is not available the code falls back to a degraded mode that keeps the GUI and frame pipeline running but won't detect hands. This is useful for exploring the app and testing platform integration without building MediaPipe.

## Video demo (coming soon)

![Video demo placeholder](https://via.placeholder.com/640x360.png?text=Video+demo+coming+soon)

## License
This repository includes a `LICENSE` file (MIT) — change or add a different license if needed.
# Finger Tracking Volume Control

Minimal repo to control system volume with finger tracking (OpenCV + MediaPipe).

Quick start
1. Install prerequisites (recommended in a venv):
   - Python 3.10+
   - pip install opencv-python mediapipe numpy pycaw comtypes

2. Option A — use the launcher (interactive):
   - python main.py
   - Choose the script to run (default recommendation: "v2").

3. Option B — run a specific script:
   - Run camera server (if using shared memory): python cameraServer.py
     - In another terminal, run: python handTrackingVolumeAdjustV2.py
   - Or run direct-capture volume control: python handTrackingVolumeAdjust.py
   - Or run basic demos: python handTrackingBasic.py or python handTrackingMeasurements.py

Notes
- The module [`handTrackingModule.HandDetector`](handTrackingModule.py) contains the hand detection utilities.
- The frame-sharing implementation is in [cameraServer.py](cameraServer.py) (server) and [`frameClient.main`](frameClient.py) (client).
- [`handTrackingVolumeAdjustV2.process_frame`](handTrackingVolumeAdjustV2.py) is the callback used by the frame client-based demo.

Video demo (coming soon)
![Video demo placeholder](https://via.placeholder.com/640x360.png?text=Video+demo+coming+soon)

License / contact
- Add your license and contact info here.