# # instaui-mermaid

<div align="center">

简体中文| [English](./README.en.md)

</div>
 
## 📖 介绍
instaui-mermaid 是 InstaUI 项目的一部分，是一个 Python 库，用于在 InstaUI 中生成 mermaid 图。

## 安装

```shell
pip install instaui-mermaid instaui[web]
```

```shell
uv add instaui-mermaid instaui[web] 
```

## 使用

```python
from instaui_mermaid import Mermaid
from instaui import ui

@ui.page("/")
def index():
    graph = r"""
    graph TD
    a --> b
"""
    # ui
    Mermaid(graph)

ui.server(debug=True).run()
```

动态更新图形：

```python
from instaui_mermaid import Mermaid
from instaui import ui, html


@ui.page("/")
def index():
    themes = ["default", "neutral", "dark", "forest", "base"]
    theme = ui.state(themes[0])

    graph = ui.str_format(
        r"""
---
config:
  theme: {theme}
---
    graph TD
    a --> b
""",
        theme=theme,
    )

    # ui
    html.select.from_list(themes, value = theme)
    Mermaid(graph)

ui.server(debug=True).run()
```


