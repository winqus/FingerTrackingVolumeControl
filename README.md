# Finger Tracking Volume Control

Control system audio using finger tracking (OpenCV + MediaPipe).
The extended pinky finger triggers audio adjustment mode, and the distance between the thumb and index finger controls the audio level.

![Demo image](docs/demo.png)

## Demo Video
<video src="https://github.com/user-attachments/assets/c6ccbca8-12fd-4430-87b6-9f8d203c4cb3" width="auto" height="auto" controls></video>

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

3. Run camera server (if using shared memory): `python cameraServer.py`

4. Recommended: use the launcher `main.py` from the repository root. It will try to import the target script and call its `main()` when available (preferred), otherwise it will spawn a subprocess.

```bash
python main.py        # interactive menu (default runs v2)
python main.py --list # list options
python main.py v2     # run the v2 demo
```

5. Or run a specific script directly:

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
