"""Check Windows commit headroom before launching the unmodified ComfyUI.

10 GiB is a conservative project launch budget based on observed ~7 GiB
Python commit at failed loading, plus headroom. It is not a model guarantee.
"""
from pathlib import Path
import ctypes
import runpy
import sys

MIN_COMMIT_GIB = 10


class MemoryStatus(ctypes.Structure):
    _fields_ = [("length", ctypes.c_uint32), ("load", ctypes.c_uint32)] + [
        (name, ctypes.c_uint64) for name in (
            "total_physical", "available_physical", "total_commit",
            "available_commit", "total_virtual", "available_virtual", "extended")]


def check_memory():
    memory = MemoryStatus()
    memory.length = ctypes.sizeof(memory)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
        raise OSError("Cannot inspect Windows memory; ComfyUI was not started.")
    available = memory.available_commit / 1024**3
    print(f"Windows available commit: {available:.2f} GiB; "
          f"available physical RAM: {memory.available_physical / 1024**3:.2f} GiB.", flush=True)
    if available < MIN_COMMIT_GIB:
        print(f"Not started: this MVP requires at least {MIN_COMMIT_GIB} GiB of "
              "available commit before loading. Save work and close unused apps, "
              "or configure a Windows page file, then retry. Do not download "
              "another model to fix this error.", file=sys.stderr, flush=True)
        return False
    return True


if __name__ == "__main__":
    if not check_memory():
        sys.exit(2)
    if "--check-memory" in sys.argv:
        sys.exit(0)
    main = (Path(__file__).resolve().parents[1] / ".local/comfy/"
            "ComfyUI_windows_portable/ComfyUI/main.py")
    sys.path.insert(0, str(main.parent))
    sys.argv[0] = str(main)
    runpy.run_path(str(main), run_name="__main__")
