"""Sphinx configuration."""
project = "Gcode Transfer"
author = "Yanxiang Gao"
copyright = "2024, Yanxiang Gao"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
