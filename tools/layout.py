"""Resolve paths recorded before the research-data layout migration."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def recorded_path(name, root=ROOT):
    """Resolve an original provenance path without editing the frozen record."""
    root = Path(root)
    layout = json.loads((root / "data/layout.json").read_text())
    return root / layout["moves"].get(str(name), {"path": str(name)})["path"]
