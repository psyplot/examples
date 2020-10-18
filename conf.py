# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import os.path as osp

from docutils import nodes
from docutils.statemachine import StringList
from sphinx.util.docutils import SphinxDirective

import nbformat
import psyplot
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "psyplot-examples"
copyright = "2020, Philipp S. Sommer"
author = "Philipp S. Sommer"

# -- Get version information and date from Git ----------------------------

try:
    from subprocess import check_output
    release = check_output(['git', 'describe', '--tags', '--always'])
    release = release.decode().strip()
    today = check_output(['git', 'show', '-s', '--format=%ad', '--date=short'])
    today = today.decode().strip()
except Exception:
    release = '<unknown>'
    today = '<unknown date>'


html_title = project + ' version ' + release


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "nbsphinx",
    "sphinx_gallery.load_style",
    "sphinx_rtd_theme",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {
    'includehidden': False,
}

# This is processed by Jinja2 and inserted before each notebook
# taken from https://github.com/spatialaudio/nbsphinx/blob/master/doc/conf.py
nbsphinx_prolog = r"""
{% set docname = env.doc2path(env.docname, base=None) %}

.. raw:: html

    <div class="admonition note">
      This page was generated from
      <a class="reference external" href="https://github.com/psyplot/examples/blob/{{ env.config.release|e }}/{{ docname|e }}">{{ docname|e }}</a>.
      <br>
      Interactive online version:
      <span style="white-space: nowrap;"><a href="https://mybinder.org/v2/gh/psyplot/examples/{{ env.config.release|e }}?filepath={{ docname|e }}"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>.</span>
      <script>
        if (document.location.host) {
          $(document.currentScript).replaceWith(
            '<a class="reference external" ' +
            'href="https://nbviewer.jupyter.org/url' +
            (window.location.protocol == 'https:' ? 's/' : '/') +
            window.location.host +
            window.location.pathname.slice(0, -4) +
            'ipynb">View in <em>nbviewer</em></a>.'
          );
        }
      </script>
    </div>

.. only:: html

    .. note::

        .. list-supplementary:: {{ docname|e }}

.. raw:: latex

    \nbsphinxstartnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{The following section was generated from
    \sphinxcode{\sphinxupquote{\strut {{ docname | escape_latex }}}} \dotfill}}
"""

# This is processed by Jinja2 and inserted after each notebook
# taken from https://github.com/spatialaudio/nbsphinx/blob/master/doc/conf.py
nbsphinx_epilog = r"""
{% set docname = 'doc/' + env.doc2path(env.docname, base=None) %}
.. raw:: latex

    \nbsphinxstopnotebook{\scriptsize\noindent\strut
    \textcolor{gray}{\dotfill\ \sphinxcode{\sphinxupquote{\strut
    {{ docname | escape_latex }}}} ends here.}}
"""

# latex elements copied from
# https://github.com/spatialaudio/nbsphinx/blob/master/doc/conf.py
latex_elements = {
    'papersize': 'a4paper',
    'printindex': '',
    'sphinxsetup': r"""
        %verbatimwithframe=false,
        %verbatimwrapslines=false,
        %verbatimhintsturnover=false,
        VerbatimColor={HTML}{F5F5F5},
        VerbatimBorderColor={HTML}{E0E0E0},
        noteBorderColor={HTML}{E0E0E0},
        noteborder=1.5pt,
        warningBorderColor={HTML}{E0E0E0},
        warningborder=1.5pt,
        warningBgColor={HTML}{FBFBFB},
    """,
    'preamble': r"""
\usepackage[sc,osf]{mathpazo}
\linespread{1.05}  % see http://www.tug.dk/FontCatalogue/urwpalladio/
\renewcommand{\sfdefault}{pplj}  % Palatino instead of sans serif
\IfFileExists{zlmtt.sty}{
    \usepackage[light,scaled=1.05]{zlmtt}  % light typewriter font from lmodern
}{
    \renewcommand{\ttdefault}{lmtt}  % typewriter font from lmodern
}
\usepackage{booktabs}  % for Pandas dataframes
""",
}


if not osp.exists("index.rst"):

  with open("index.rst", "w") as f:
    f.write("""
.. _examples:

.. include:: README.rst

.. toctree::
  :hidden:
  :glob:

  README.rst
  general/*
  simple/*
  maps/*
  regression-analysis/*

.. nbgallery::
    :name: Example Gallery
    :glob:
    :reversed:

    general/example_*
    simple/example_*
    maps/example_*
    regression-analysis/example_*
""")

  os.makedirs("_static", exist_ok=True)


# add a directive for supplementary files (this is used in the prolog above)
class SupplementaryDirective(SphinxDirective):
    """A directive to list supplementary files

    Usage::

        .. list-supplementary:: <path-to-notebook>
    """

    has_content = False

    required_arguments = 1

    def add_line(self, line: str) -> None:
        """Append one line of generated reST to the output."""
        source = self.get_source_info()
        if line.strip():  # not a blank line
            self.result.append(line, *source)
        else:
            self.result.append('', *source)

    def generate(self) -> None:
        """Generate the content."""

        infile = self.arguments[0]

        nb = nbformat.read(infile, nbformat.current_nbformat)
        files = getattr(nb.metadata, 'supplementary_files', None)

        if files:
            if len(files) == 1:
                self.add_line(
                    f"This example requires the :download:`{files[0]}` file."
                )
            else:
              self.add_line("This examples needs the following files:")
              self.add_line("")
              for f in files:
                  self.add_line(f"- :download:`{f}`")

    def run(self):
        """Run the directive."""
        reporter = self.state.document.reporter

        self.result = StringList()

        self.generate()

        node = nodes.paragraph()
        node.document = self.state.document
        self.state.nested_parse(self.result, 0, node)

        return node.children


def setup(app):
    app.add_directive('list-supplementary', SupplementaryDirective)