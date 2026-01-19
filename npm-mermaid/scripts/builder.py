from pathlib import Path
from shutil import copyfile, rmtree

PORJECT_ROOT = Path(__file__).parent.parent.resolve()
PY_PROJECT_ROOT = PORJECT_ROOT.parent
PY_STATIC_PATH = PY_PROJECT_ROOT.joinpath("src/instaui_mermaid/static").resolve()

NODE_MERMAID_DIST_PATH = PORJECT_ROOT / "node_modules" / "mermaid" / "dist"
DIST_PATH = PORJECT_ROOT.joinpath("dist").resolve()

CHUNKS_DIR = PY_STATIC_PATH / "chunks" / "mermaid.esm.min"

MAIN_FILE = DIST_PATH.joinpath("instaui-mermaid.js")
MAIN_MAP_FILE = DIST_PATH.joinpath("instaui-mermaid.js.map")

MERMAID_MIN_FILE = NODE_MERMAID_DIST_PATH.joinpath("mermaid.esm.min.mjs")
MERMAID_CHUNKS_DIR = NODE_MERMAID_DIST_PATH / "chunks" / "mermaid.esm.min"


def copy_to_static():
    copyfile(MAIN_FILE, PY_STATIC_PATH.joinpath(MAIN_FILE.name))
    if MAIN_MAP_FILE.exists():
        copyfile(MAIN_MAP_FILE, PY_STATIC_PATH.joinpath(MAIN_MAP_FILE.name))

    copyfile(MERMAID_MIN_FILE, PY_STATIC_PATH.joinpath(MERMAID_MIN_FILE.name))
    if CHUNKS_DIR.exists():
        rmtree(CHUNKS_DIR)

    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    for file in MERMAID_CHUNKS_DIR.glob("*.mjs"):
        copyfile(file, CHUNKS_DIR.joinpath(file.name))


def copy2py():
    copy_to_static()
    print(f"Copied to static folder [{PY_STATIC_PATH}]")


if __name__ == "__main__":
    copy2py()
