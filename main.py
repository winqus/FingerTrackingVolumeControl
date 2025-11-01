#!/usr/bin/env python3
"""Launcher for FingerTrackingVolumeControl demos.

Tries to import target module and call its `main()` if present. Falls back to spawning a subprocess.
"""
import sys
import subprocess
import importlib
import argparse
import os

SCRIPTS = {
    "v2": ("handTrackingVolumeAdjustV2", "handTrackingVolumeAdjustV2.py"),
    "v1": ("handTrackingVolumeAdjust", "handTrackingVolumeAdjust.py"),
    "basic": ("handTrackingBasic", "handTrackingBasic.py"),
    "measure": ("handTrackingMeasurements", "handTrackingMeasurements.py"),
    "server": ("cameraServer", "cameraServer.py"),
    "example-client": ("exampleFrameClientUse", "exampleFrameClientUse.py"),
    "frame-client": ("frameClient", "frameClient.py"),
}


def list_scripts():
    print("Available scripts:")
    for name, (_, path) in SCRIPTS.items():
        print(f"  {name:15} -> {path}")
    print()


def run_module(module_name, script_path):
    """Try to import module and call its main(), otherwise spawn subprocess."""
    cwd = os.getcwd()
    # Attempt import
    try:
        if cwd not in sys.path:
            sys.path.insert(0, cwd)
        mod = importlib.import_module(module_name)
        if hasattr(mod, "main"):
            print(f"Importing and running {module_name}.main()")
            # Call main() with no args; modules should accept optional args
            try:
                mod.main()
                return 0
            except TypeError:
                # fallback if main requires args
                mod.main()
                return 0
    except Exception as e:
        print(f"Import-run failed for {module_name}: {e}")

    # Fallback: spawn subprocess
    print(f"Falling back to subprocess: {script_path}")
    return subprocess.run([sys.executable, script_path]).returncode


def main():
    parser = argparse.ArgumentParser(description="Launcher for FingerTrackingVolumeControl demos")
    parser.add_argument("script", nargs="?", help="Script key to run (see --list)")
    parser.add_argument("--list", action="store_true", help="List available scripts")
    args = parser.parse_args()

    if args.list:
        list_scripts()
        return 0

    if args.script:
        key = args.script
        mapping = SCRIPTS.get(key)
        if not mapping:
            print("Unknown script key. Use --list to see options.")
            return 2
        module_name, path = mapping
        return run_module(module_name, path)

    # interactive
    list_scripts()
    choice = input("Choose script to run (default: v2) > ").strip() or "v2"
    mapping = SCRIPTS.get(choice)
    if not mapping:
        print("Unknown choice.")
        return 2
    module_name, path = mapping
    return run_module(module_name, path)


if __name__ == "__main__":
    sys.exit(main())
import sys
import subprocess
import argparse
import os

SCRIPTS = {
    "v2": "handTrackingVolumeAdjustV2.py",
    "v1": "handTrackingVolumeAdjust.py",
    "basic": "handTrackingBasic.py",
    "measure": "handTrackingMeasurements.py",
    "server": "cameraServer.py",
    "example-client": "exampleFrameClientUse.py"
}

def list_scripts():
    print("Available scripts:")
    for name, path in SCRIPTS.items():
        print(f"  {name:15} -> {path}")
    print()

def run_script(path):
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return 1
    try:
        return subprocess.run([sys.executable, path]).returncode
    except KeyboardInterrupt:
        print("Interrupted.")
        return 1

def interactive_menu():
    list_scripts()
    choice = input("Choose script to run (default: v2) > ").strip() or "v2"
    script = SCRIPTS.get(choice)
    if not script:
        print("Unknown choice.")
        return 1
    print(f"Running {script}...")
    return run_script(script)

def main():
    parser = argparse.ArgumentParser(description="Launcher for FingerTrackingVolumeControl demos")
    parser.add_argument("script", nargs="?", help="Script key to run (see --list)")
    parser.add_argument("--list", action="store_true", help="List available scripts")
    args = parser.parse_args()

    if args.list:
        list_scripts()
        return 0

    if args.script:
        script = SCRIPTS.get(args.script)
        if not script:
            print("Unknown script key. Use --list to see options.")
            return 1
        return run_script(script)

    # no args -> interactive
    return interactive_menu()

if __name__ == "__main__":
    sys.exit(main())