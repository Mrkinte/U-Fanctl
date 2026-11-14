import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
OUTPUT_PATH = REPO_ROOT / "webui" / "openapi.json"

sys.path.insert(0, str(SRC_DIR))

from fanctl.app import create_app  # noqa: E402


def main() -> None:
    schema = create_app().openapi()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(schema, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"OpenAPI schema written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
