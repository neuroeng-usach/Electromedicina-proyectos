# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options.
# For a full list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------
# If your docs need to import your Python package (e.g. for autodoc),
# uncomment and adjust the path below to point at your source root.
# sys.path.insert(0, os.path.abspath('../..'))


# -- Project information ------------------------------------------------------

project = "My Project"
copyright = "2026, Your Name or Organization"
author = "Your Name or Organization"

# The full version, including alpha/beta/rc tags
release = "0.1.0"
# The short X.Y version
version = "0.1.0"


# -- General configuration ----------------------------------------------------

extensions = [
    "myst_parser",              # Parse Markdown (.md) files
    "sphinx.ext.autodoc",       # Pull docstrings from your code (optional)
    "sphinx.ext.napoleon",      # Google/NumPy style docstrings (optional)
    "sphinx.ext.viewcode",      # Add links to highlighted source code
    "sphinx.ext.intersphinx",   # Link to other projects' docs
    "sphinx_copybutton",        # Copy button on code blocks (optional, pip install sphinx-copybutton)
]

# Recognize both .md and .rst as source files
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# MyST (Markdown) extensions - enables GitHub-Flavored-Markdown-like features
myst_enable_extensions = [
    "colon_fence",      # ::: fenced directives
    "deflist",          # definition lists
    "html_image",       # allow raw <img> tags
    "linkify",          # auto-detect bare URLs as links
    "replacements",     # smart quotes/typography
    "substitution",     # {{ variable }} substitutions
    "tasklist",         # - [ ] task lists
]

# Automatically generate heading anchors up to this depth (useful for
# in-page markdown links like [text](#some-heading))
myst_heading_anchors = 3

# The master/root document
root_doc = "index"

# Patterns to exclude from the build
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".venv",
    "venv",
]

# The suffix(es) of source filenames handled above via source_suffix
templates_path = ["_templates"]

# If you use Jupyter-style notebooks via myst-nb, add "myst_nb" to
# extensions instead of / alongside "myst_parser".


# -- Options for HTML output ---------------------------------------------------

# Read the Docs supplies its own theme injection, but declaring it here
# keeps local `make html` builds looking the same as the RTD build.
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "collapse_navigation": False,
    "navigation_depth": 4,
    "titles_only": False,
}

html_static_path = ["_static"]

# Uncomment and add a logo/favicon if you have one in _static/
# html_logo = "_static/logo.png"
# html_favicon = "_static/favicon.ico"


# -- Intersphinx mapping (optional) --------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}


# -- Read the Docs specific tweaks ---------------------------------------------

# When building on Read the Docs, this environment variable is set to "True".
on_rtd = os.environ.get("READTHEDOCS") == "True"

if on_rtd:
    # Example: adjust behavior specifically for RTD builds if needed.
    pass
