"""Cross-platform audio control helpers.

Exports:
  - set_volume(percent: int|float) -> None
  - get_volume() -> int

Implementations:
  - Windows: use pycaw (if installed)
  - macOS: use AppleScript via `osascript`
  - Linux: try `amixer` if available
  - Fallback: no-op with logging
"""
from typing import Union
import sys
import subprocess
import shutil
import logging

logger = logging.getLogger(__name__)

def _to_int(value: Union[int, float]) -> int:
    try:
        return int(round(float(value)))
    except Exception:
        return 0

# Try Windows pycaw implementation
_HAS_PYCAW = False
try:
    if sys.platform.startswith("win"):
        from comtypes import CLSCTX_ALL  # type: ignore
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # type: ignore
        _HAS_PYCAW = True
except Exception:
    _HAS_PYCAW = False


def _windows_get_set_volume(percent: Union[int, float] = None):
    # Use pycaw to get/set master volume as scalar (0.0 - 1.0)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volumeInterface = interface.QueryInterface(IAudioEndpointVolume)
    if percent is None:
        return int(round(volumeInterface.GetMasterVolumeLevelScalar() * 100))
    else:
        volumeInterface.SetMasterVolumeLevelScalar(max(0.0, min(1.0, float(percent) / 100.0)), None)
        return None


def _darwin_get_volume():
    # Use AppleScript to get output volume
    try:
        out = subprocess.check_output(["osascript", "-e", "output volume of (get volume settings)"])
        return int(out.decode().strip())
    except Exception as e:
        logger.debug("osascript get volume failed: %s", e)
        return 0


def _darwin_set_volume(percent: Union[int, float]):
    p = _to_int(percent)
    try:
        subprocess.check_call(["osascript", "-e", f'set volume output volume {p}'])
    except Exception as e:
        logger.debug("osascript set volume failed: %s", e)


def _linux_get_volume():
    # Try amixer
    amixer = shutil.which("amixer")
    if not amixer:
        return 0
    try:
        out = subprocess.check_output([amixer, "sget", "Master"]).decode()
        # parse like: [66%]
        import re
        m = re.search(r"(\d{1,3})%", out)
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return 0


def _linux_set_volume(percent: Union[int, float]):
    amixer = shutil.which("amixer")
    if not amixer:
        return
    p = _to_int(percent)
    try:
        subprocess.check_call([amixer, "sset", "Master", f"{p}%"])
    except Exception as e:
        logger.debug("amixer set volume failed: %s", e)


def get_volume() -> int:
    """Return system master volume as integer percent (0-100).

    If platform-specific backend is unavailable, returns 0.
    """
    if _HAS_PYCAW and sys.platform.startswith("win"):
        try:
            return _windows_get_set_volume(None)
        except Exception:
            logger.debug("pycaw get failed", exc_info=True)

    if sys.platform == "darwin":
        return _darwin_get_volume()

    if sys.platform.startswith("linux"):
        return _linux_get_volume()

    # Fallback
    logger.debug("No audio backend available for get_volume on platform %s", sys.platform)
    return 0


def set_volume(percent: Union[int, float]):
    """Set system master volume (0-100)."""
    if percent is None:
        return
    if _HAS_PYCAW and sys.platform.startswith("win"):
        try:
            _windows_get_set_volume(percent)
            return
        except Exception:
            logger.debug("pycaw set failed", exc_info=True)

    if sys.platform == "darwin":
        _darwin_set_volume(percent)
        return

    if sys.platform.startswith("linux"):
        _linux_set_volume(percent)
        return

    logger.debug("No audio backend available for set_volume on platform %s", sys.platform)


if __name__ == "__main__":
    # Quick smoke: print volume and attempt to set 30 then restore
    cur = get_volume()
    print("Current volume:", cur)
    print("Setting volume to 30 (test)")
    set_volume(30)
    print("Now:", get_volume())
    set_volume(cur)
