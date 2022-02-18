# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'Dexter'
copyright = '2022 Selfdual Technologies'
author = 'Wojciech Klaudiusz Zaborowski'

release = '1.0'
version = '1'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.imgconverter'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# -- Options for LaTeX output ---------------------------------------------

mathjax3_config = {
    'chtml' : {
        'scale' : 0.8,
    }
}

# -- Options for HTML output ---------------------------------------------
html_theme = 'sphinx_rtd_theme