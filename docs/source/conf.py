#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# conx documentation build configuration file
#

import io
import os
import sys
import glob
import shutil

sys.path.insert(0, os.path.abspath('../..'))

## dependencies: get ../../notebooks/*.ipynb files

print("Copying updated ../../notebooks/ files ...")
for filename in (glob.glob("../../notebooks/*.ipynb") +
                 glob.glob("../../*.md") +
                 glob.glob("../../notebooks/*.gif") +
                 glob.glob("../../notebooks/*.jpg") +
                 glob.glob("../../notebooks/*.png")):
    path, dst = os.path.split(filename)
    if os.path.isfile(dst): # dst exists here
        dst_time = os.path.getmtime(dst)
        src_time = os.path.getmtime(filename)
        if src_time > dst_time: # the src time > dst time
            copy_it = True # it is updated
        else:
            copy_it = False # not updated
    else:
        copy_it = True # doesn't exist
    if copy_it:
        shutil.copyfile(filename, dst)
        print("   ", dst)

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'nbsphinx',
    'jupyter_sphinx.embed_widgets',
    'sphinxcontrib.napoleon',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

source_parsers = {
   '.md': 'recommonmark.parser.CommonMarkParser',
}

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']
# source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'conx'
copyright = '2017, Douglas Blank'
author = 'Douglas Blank'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '3.0'
# The full version, including alpha/beta/rc tags.
release = '3.0.1'

with io.open('../../conx/_version.py', encoding='utf-8') as fid:
    for line in fid:
        if line.startswith('__version__'):
            release = line.strip().split()[-1][1:-1]
            break
version = ".".join(release.split(".")[:2])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

html_static_path = ['_static']
# html_theme_options = {}

def setup(app):
    app.add_stylesheet('css/custom.css')

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'conxdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'conx.tex', 'conx Documentation',
     'Douglas Blank', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'conx', 'conx Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'conx', 'conx Documentation',
     author, 'conx', 'One line description of project.',
     'Miscellaneous'),
]




# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}
