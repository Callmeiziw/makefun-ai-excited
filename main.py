"""Copy entry.png (next to this script) into the make.fun output directory."""

import os
import shutil
from pathlib import Path

import sys

SRC = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1024 * 1024  # 1 MiB
PNG_SIG = b"\x89PNG\r\n\x1a\n"
JPEG_SIG = b"\xff\xd8\xff"


def validate(path: Path) -> None:
    size = path.stat().st_size
    if size == 0 or size > MAX_BYTES:
        raise ValueError(f"{path.name}: invalid size {size} bytes (max {MAX_BYTES})")
    with path.open("rb") as f:
        head = f.read(8)
    if not (head.startswith(PNG_SIG) or head.startswith(JPEG_SIG)):
        raise ValueError(f"{path.name}: not a PNG or JPEG file")


def main() -> int:
    try:
        validate(SRC)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, out_dir / "entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
