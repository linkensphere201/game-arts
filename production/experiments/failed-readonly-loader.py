raise SystemExit("Archived failed experiment; disabled. See README.md.")
"""Project-local readonly safetensors loader for Windows without a pagefile.

Keeps verified weights file-backed instead of committing a private writable copy.
The original portable utils.py is retained; no system settings are changed.
"""
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[1]
path = ROOT / '.local/comfy/ComfyUI_windows_portable/ComfyUI/comfy/utils.py'
backup = path.with_suffix('.py.original')
if not backup.exists():
    shutil.copy2(path, backup)
source = backup.read_text(encoding='utf-8')
marker = 'def load_torch_file(ckpt, safe_load=False, device=None, return_metadata=False):'
helper = '''# Project-local Windows read-only loader; enabled only by explicit environment flag.
_GAME_ARTS_MAPPINGS = {}

def load_game_arts_readonly(ckpt):
    import mmap
    if ckpt not in _GAME_ARTS_MAPPINGS:
        handle = open(ckpt, "rb")
        mapped = mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ)
        _GAME_ARTS_MAPPINGS[ckpt] = (handle, mapped)
    mapped = _GAME_ARTS_MAPPINGS[ckpt][1]
    if len(mapped) < 8:
        raise ValueError("Incomplete safetensors file")
    header_size = struct.unpack("<Q", mapped[:8])[0]
    base = 8 + header_size
    if header_size > 100_000_000 or base > len(mapped):
        raise ValueError("Invalid safetensors header")
    header = json.loads(mapped[8:base])
    view = memoryview(mapped)
    state = {}
    for key, info in header.items():
        if key == "__metadata__":
            continue
        start, end = info["data_offsets"]
        dtype = _TYPES[info["dtype"]]
        if not (0 <= start <= end <= len(mapped) - base):
            raise ValueError("Tensor range outside file")
        if math.prod(info["shape"]) * dtype.itemsize != end - start:
            raise ValueError("Tensor size mismatch")
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="The given buffer is not writable")
            state[key] = (torch.frombuffer(view[base+start:base+end], dtype=dtype).view(info["shape"])
                          if end > start else torch.empty(info["shape"], dtype=dtype))
    return state, header.get("__metadata__", {})

'''
needle = '            if comfy.memory_management.aimdo_enabled:\n'
replacement = '''            if os.environ.get("GAME_ARTS_READONLY_SAFETENSORS") == "1":
                sd, metadata = load_game_arts_readonly(ckpt)
                if not return_metadata:
                    metadata = None
            elif comfy.memory_management.aimdo_enabled:
'''
if source.count(needle) != 1 or source.count(marker) != 1:
    raise RuntimeError('Unexpected ComfyUI source; inspect before patching')
path.write_text(source.replace(marker, helper + marker).replace(needle, replacement), encoding='utf-8')
print('Project-local readonly loader installed; original retained')
