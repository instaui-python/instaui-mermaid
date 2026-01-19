from typing import Callable, Optional
from instaui import ui, html
from dataclasses import dataclass
from __tests.testing_web.context import Context


@dataclass
class ComputedStyleResult:
    value: str
    create_button: Callable[[], html.button]

    el: ui.element_ref


def use_computed_style(style_name: str, *, target_selector: Optional[str] = None):
    style_value = ui.state("")
    ele = ui.element_ref()

    on_update = ui.js_event(
        inputs=[ele, style_name, target_selector],
        outputs=[style_value],
        code=r"""(ele, style_name,target_selector)=> {
    const target = target_selector ? document.querySelector(target_selector) : (ele.$el ?? ele);
    const value = window.getComputedStyle(target).getPropertyValue(style_name)                      
    return value;
}""",
    )

    def create_button():
        return html.button("update style").on_click(on_update)

    return ComputedStyleResult(style_value, create_button, ele)


def update_style(context: Context):
    context.find_by_text("update style").click()
