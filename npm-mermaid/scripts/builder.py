from pathlib import Path
from shutil import copyfile, rmtree


NODE_MERMAID_DIST_PATH = (
    Path(__file__).parent.parent / "node_modules" / "mermaid" / "dist"
)
DIST_PATH = Path(__file__).parent.joinpath("../dist").resolve()

PY_DIR = Path(__file__).parent.joinpath("../../src/mermaid").resolve()
STATIC_PATH = PY_DIR.joinpath("static").resolve()
CHUNKS_DIR = STATIC_PATH / "chunks" / "mermaid.esm.min"


MAIN_FILE = DIST_PATH.joinpath("instaui-mermaid.js")
MAIN_MAP_FILE = DIST_PATH.joinpath("instaui-mermaid.js.map")

MERMAID_MIN_FILE = NODE_MERMAID_DIST_PATH.joinpath("mermaid.esm.min.mjs")
MERMAID_CHUNKS_DIR = NODE_MERMAID_DIST_PATH / "chunks" / "mermaid.esm.min"


def copy_to_static():
    copyfile(MAIN_FILE, PY_DIR.joinpath(MAIN_FILE.name))
    if MAIN_MAP_FILE.exists():
        copyfile(MAIN_MAP_FILE, PY_DIR.joinpath(MAIN_MAP_FILE.name))

    copyfile(MERMAID_MIN_FILE, STATIC_PATH.joinpath(MERMAID_MIN_FILE.name))
    if CHUNKS_DIR.exists():
        rmtree(CHUNKS_DIR)

    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    for file in MERMAID_CHUNKS_DIR.glob("*.mjs"):
        copyfile(file, CHUNKS_DIR.joinpath(file.name))


def copy2py():
    copy_to_static()
    print(f"Copied to static folder [{STATIC_PATH}]")


if __name__ == "__main__":
    copy2py()
