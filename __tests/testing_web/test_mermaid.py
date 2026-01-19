from __tests.testing_web.context import Context
from instaui import ui, html
from instaui_mermaid import Mermaid
from __tests.layout_testing_utils import update_style, use_computed_style


def test_base(context: Context):
    @context.register_page
    def index():
        graph = r"""
        graph TD
        foo --> bar
    """
        Mermaid(graph)

    context.open()
    context.should_see("foo")
    context.should_see("bar")


def test_frontmatter_configuration(context: Context):
    @context.register_page
    def index():
        use_style = use_computed_style("color", target_selector=".target .nodeLabel p")
        themes = ["default", "dark"]
        theme = ui.state(themes[0])

        graph = ui.str_format(
            r"""
---
config:
    theme: {theme}
---
    graph TD
    foo:::target
    """,
            theme=theme,
        )

        html.select.from_list(themes, theme)
        use_style.create_button()
        ui.text(use_style.value)
        Mermaid(graph)

    context.open()
    context.should_see("foo")

    update_style(context)
    context.should_see("rgb(51, 51, 51)")

    context.find("combobox").select_option("dark")
    update_style(context)
    context.should_see("rgb(204, 204, 204)")


def test_node_click(context: Context):
    @context.register_page
    def index():
        graph = r"""
        graph TD
        foo
        """

        text = ui.state("")

        @ui.event(inputs=[ui.event_context.e()], outputs=[text])
        def click_foo(e):
            return e["arg"]

        ui.text(text)
        Mermaid(
            graph, node_click_configs=[{"node": "foo", "arg": "this is foo"}]
        ).on_node_click(click_foo)

    context.open()
    context.should_see("foo")
    context.find_by_text("foo").click()
    context.should_see("this is foo")
