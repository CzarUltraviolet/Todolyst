import sys
import os

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Todolyst'
copyright = '2023, Frédéric_Lauron Pascal_Mahé Yannick_Letort Pierre_DLVM'
author = 'Frédéric_Lauron Pascal_Mahé Yannick_Letort Pierre_DLVM'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',"sphinx.ext.viewcode","sphinx.ext.napoleon"]

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../todolyst/*'))
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


html_theme_options = {
    "logo": "Logo-Télécom-Paris-IP-Paris_light.png",
    
	
}
