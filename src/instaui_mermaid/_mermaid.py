from __future__ import annotations
from pathlib import Path
from typing import ClassVar, TypedDict, cast
from instaui import ui
from instaui.internal.ui.event import EventMixin

_STATIC_DIR = Path(__file__).parent / "static"
_MERMAID_JS_FILE = _STATIC_DIR / "mermaid.esm.min.mjs"


_IMPORT_MAPS = {"mermaid": _MERMAID_JS_FILE}


class Mermaid(
    ui.element,
    esm="./instaui-mermaid.js",
    externals=_IMPORT_MAPS,
):
    """
    A UI component to render Mermaid diagrams from text-based syntax.

    Args:
        graph (str): A string containing the Mermaid diagram definition.
                     This defines the structure and appearance of the diagram using Mermaid's syntax.

    Example:
    .. code-block:: python
        from instaui import ui
        from instaui_mermaid import Mermaid

        @ui.page()
        def home():
            graph = '''
            graph TB
            FullFirstSquad-->StripedFirstSquad
            '''
            Mermaid(graph)
    """

    CONFIG: ClassVar[TMermaidConfig | None] = None

    def __init__(
        self,
        graph: str,
        *,
        node_clickables: list[TNodeClickable] | NodeClickable | None = None,
    ):
        super().__init__()
        node_clickables = (
            node_clickables.configs
            if isinstance(node_clickables, NodeClickable)
            else node_clickables
        )
        self.props(
            {
                "graph": graph,
                "clickConfigs": node_clickables,
                "initConfig": self.CONFIG or None,
            }
        )

    def on_node_click(self, handler: EventMixin):
        return self.on("node:click", handler)


def mermaid_config(*, theme: str | None = None):
    config = {}
    if theme:
        config["theme"] = theme

    if config:
        Mermaid.CONFIG = cast(TMermaidConfig, config)


class TMermaidConfig(TypedDict, total=False):
    theme: str


class NodeClickable:
    configs: list[TNodeClickable] = []

    @classmethod
    def create(cls, node: str, arg: str | None = None) -> NodeClickable:
        ins = cls()
        ins.configs = [*cls.configs, {"node": node, "arg": arg}]
        return ins


class TNodeClickable(TypedDict, total=False):
    node: str
    arg: str | None
