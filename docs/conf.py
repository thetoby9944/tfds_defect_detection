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
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath('../tfds_defect_detection'))
# sys.path.insert(0, os.path.abspath('../../modules/'))


# -- Project information -----------------------------------------------------

project = 'TFDS Defect Detection'
copyright = '2022, Tobias Schiele'
author = 'Tobias Schiele'

# The full version, including alpha/beta/rc tags
release = '0.1.0'

# -- Internationalization ------------------------------------------------
# specifying the natural language populates some key tags
language = "en"


# -- General configuration ---------------------------------------------------

# Allows using numbered figures in latex and html output
numfig = True

# Root document containing initial toc
master_doc = "index"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "recommonmark",  # Allow processing md files
    'sphinx.ext.viewcode',  # Link sources to documentation
    'autoapi.extension',  # generate documentation from docstrings
    'sphinx_markdown_tables',  # allow markdown style tables (only works for html output sadly)
    'sphinx.ext.napoleon',
    #'sphinxcontrib.autohttp.web', # generate web endpoints from source code
    #'sphinxcontrib.bibtex',  # Allows using :cite:`bibtexentry` in .rst files
]


# Map file-extensions to sphinx parser
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# -- AUTOAPI ---------------------------------------------------

autoapi_type = 'python'
autoapi_dirs = [
    "../tfds_defect_detection",
    #"../../modules/"
]
autoapi_ignore = []#"*/lib/*", "*/playground/*", "*/model/*", "*/models/*", "*/nima/*", "*/qtclient/*", "*webclient/config*"]
autoapi_template_dir = '_templates'
autoapi_add_toctree_entry = True
autoapi_member_order = "groupwise"
autoapi_keep_files = True
autoapi_options =  [ 'members', 'undoc-members', 'show-inheritance', 'show-module-summary', 'special-members', ]
# autodoc_inherit_docstrings = False


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    "autoapi/index.rst",
    "requirements.txt",
    "README.md"
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

#extensions.append('sphinx_typo3_theme')
#html_theme = 'sphinx_typo3_theme'

import sphinx_bootstrap_theme

# Activate the theme.
#html_theme = 'bootstrap'
#html_theme_path = [sphinx_bootstrap_theme.get_html_theme_path()]

#extensions.append( "sphinxawesome_theme")
#html_theme =  "sphinxawesome_theme"

html_theme = "pydata_sphinx_theme" #
html_logo = "images/logo.png"
html_favicon = 'images/icon.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
html_sidebars = {'index': ["search-field.html", 'sidebar-nav-bs.html']}


html_theme_options = {
    "github_url": "https://github.com/thetoby9944/tfds_defect_detection",
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/tfds_defect_detection",
            "icon": "fas fa-box",
        },
    ],
    "use_edit_page_button": True,
    "show_toc_level": 2,
    "show_nav_level": 2,
    # "search_bar_position": "navbar",  # TODO: Deprecated - remove in future version
    # "navbar_align": "left",  # [left, content, right] For testing that the navbar items align properly
    # "navbar_start": ["navbar-logo", "navbar-version"],
    # "navbar_center": ["navbar-nav", "navbar-version"],  # Just for testing
    "navbar_end": ["navbar-icon-links"],
}

html_context = {
    "github_user": "thetoby9944",
    "github_repo": "tfds_defect_detection",
    "github_version": "master",
    "doc_path": "docs",
}

# -- Options for Latex output -------------------------------------------------

#latex_docclass = {
#   'howto': 'ausarbeitung',
#   'manual': 'ausarbeitung',
#}

asset_src = Path("../tfds_defect_detection/assets/images")

for dst in [
    Path("tfds_defect_detection/assets/images"),
    Path("assets/images"),
    Path("images"),
]:
    try:
        shutil.rmtree(dst)
    except:
        pass
    try:
        shutil.copytree(asset_src, dst)
    except:
        pass


latex_documents = [
    (master_doc, 'master.tex', u'TFDS Defect Detection',
     u'Tobias Schiele', 'report'), #"report"
]

latex_logo = 'tfds_defect_detection/assets/images/logo.png'
latex_engine = 'lualatex'
latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'a4paper',
    'releasename':" ",

    # Sonny, Lenny, Glenn, Conny, Rejne, Bjarne and Bjornstrup
    #'fncychap': '\\usepackage[Glenn]{fncychap}',
    #'fncychap': '\\usepackage{fncychap}',
    'fontpkg': '\\usepackage{amsmath,amsfonts,amssymb,amsthm}',

    # Latex figure (float) alignment
    #
    'figure_align':'htbp',

    # The font size ('10pt', '11pt' or '12pt').
    #
    'pointsize': '12pt',

    'inputenc': '',
    'utf8extra': '',


    # Additional stuff for the LaTeX preamble.
    #
    'preamble': r'''
        %%%%%%%%%%%%%%%%%%%% Meher %%%%%%%%%%%%%%%%%%
        %%%add number to subsubsection 2=subsection, 3=subsubsection
        %%% below subsubsection is not good idea.
        \setcounter{secnumdepth}{3}
        %

 
        \setmainfont{roboto}
        %\setmonofont[Colour=A0203A]{roboto}
        
        \let\oldtexttt\texttt% Store \texttt
        \renewcommand{\texttt}[2][darkgray]{\textcolor{#1}{\ttfamily #2}}% \texttt[<color>]{<stuff>}
    
        
        %%%% Table of content upto 2=subsection, 3=subsubsection
        \setcounter{tocdepth}{2}

        \usepackage{amsmath,amsfonts,amssymb,amsthm}
        \usepackage{graphicx}

        %%% reduce spaces for Table of contents, figures and tables
        %%% it is used "\addtocontents{toc}{\vskip -1.2cm}" etc. in the document
 
        \usepackage[notlot,nottoc,notlof]{}

        \usepackage{color}
        \usepackage{transparent}
        \usepackage{eso-pic}
        \usepackage{lipsum}
        \usepackage{fontspec}
        %\usepackage{utf8}[inputenc]

        \usepackage{footnotebackref} %%link at the footnote to go to the place of footnote in the text

        %% spacing between line
        \usepackage{setspace}
        %%%%\onehalfspacing
        %%%%\doublespacing
        \singlespacing


        %%%%%%%%%%% datetime
        \usepackage{datetime}

        \newdateformat{MonthYearFormat}{%
        \monthname[\THEMONTH], \THEYEAR}


        %% RO, LE will not work for 'oneside' layout.
        %% Change oneside to twoside in document class
        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \fancyhf{}

        %%% Alternating Header for oneside
        \fancyhead[L]{\ifthenelse{\isodd{\value{page}}}{ \small \nouppercase{\leftmark} }{}}
        \fancyhead[R]{\ifthenelse{\isodd{\value{page}}}{}{ \small \nouppercase{\rightmark} }}

        %%% Alternating Header for two side
        %\fancyhead[RO]{\small \nouppercase{\rightmark}}
        %\fancyhead[LE]{\small \nouppercase{\leftmark}}

        %% for oneside: change footer at right side. If you want to use Left and right then use same as header defined above.
        \fancyfoot[R]{\ifthenelse{\isodd{\value{page}}}{{\tiny Tobias Schiele} }{}}

        %%% Alternating Footer for two side
        %\fancyfoot[RO, RE]{\scriptsize Tobias Schiele}

        %%% page number
        \fancyfoot[CO, CE]{\thepage}

        \renewcommand{\headrulewidth}{0.5pt}
        \renewcommand{\footrulewidth}{0.5pt}

        \RequirePackage{tocbibind} %%% comment this to remove page number for following
        \addto\captionsenglish{\renewcommand{\contentsname}{Table of contents}}
        \addto\captionsenglish{\renewcommand{\listfigurename}{List of figures}}
        \addto\captionsenglish{\renewcommand{\listtablename}{List of tables}}
        % \addto\captionsenglish{\renewcommand{\chaptername}{Chapter}}


        %%reduce spacing for itemize
        \usepackage{enumitem}
        \setlist{nosep}

        %%%%%%%%%%% Quote Styles at the top of chapter
        \usepackage{epigraph}
        \setlength{\epigraphwidth}{0.8\columnwidth}
        \newcommand{\chapterquote}[2]{\epigraphhead[60]{\epigraph{\textit{#1}}{\textbf {\textit{--#2}}}}}
        %%%%%%%%%%% Quote for all places except Chapter
        \newcommand{\sectionquote}[2]{{\quote{\textit{``#1''}}{\textbf {\textit{--#2}}}}}
        
        %\usepackage{ragged2e}
        
        %\usepackage{microtype}
        
        %\RaggedRight
        
        %\sloppypar
        
        %\let\origbs\textbackslash
        %\newcommand\allowbreaksafterbackslashinliterals {%
        %  \def\.{\discretionary{\origbs}{}{\origbs}}% breaks after \
        %}%
        %\makeatletter
        %\g@addto@macro\sphinx@literal@nolig@list{\allowbreaksafterbackslashinliterals}
        %\makeatother
        
        \renewcommand*\sphinxbreaksafteractivelist {\do\.\do\,\do\;\do\?\do\!\do\/\do\=}
        
        
        \usepackage{xparse}

        \ExplSyntaxOn
        \NewDocumentCommand{\replace}{mmm}
         {
          \marian_replace:nnn {#1} {#2} {#3}
         }
        
        \tl_new:N \l_marian_input_text_tl
        
        \cs_new_protected:Npn \marian_replace:nnn #1 #2 #3
         {
          \tl_set:Nn \l_marian_input_text_tl { #1 }
          \tl_replace_all:Nnn \l_marian_input_text_tl { #2 } { #3 }
          \tl_use:N \l_marian_input_text_tl
         }
        \ExplSyntaxOff
        
        \usepackage{url}
        \let\OldTexttt\texttt
        \renewcommand{\texttt}[1]{\OldTexttt{\replace{#1}{.}{\allowbreak.}}}
        \let\OldPySigLine\sphinxupquote
        \renewcommand*\sphinxupquote[1]{\OldPySigLine{\replace{#1}{=}{=\allowbreak}}}
        
    ''',

    # Latex title
    # + Toc, tof, lot
    #
    'maketitle': r"""

    
    \pagenumbering{Roman} %%% to avoid page 1 conflict with actual page 1

    %--- Title page


    \begin{titlepage}
    %
        \includegraphics[scale=0.3]{../../images/hs-aalen.png} 
        % \vskip 0.5cm 
        % \hfill
        % \includegraphics[scale=0.3]{../../images/imfaa-logo.png}
        \vskip 2cm
    %
        \begin{flushleft}
            \par \color{darkgray} % \large 
            Work in progress under the scope of the dissertation \\%
            \textit{Transferring Deep Learning Technology to Industry}
            %Institute of Materials Science
        \end{flushleft}
        \vfill
    %
        \begin{center}
            %\textbf{\Huge {A Dissertation Project}}

            \vspace{0mm}
            \begin{figure}[!h]
                \centering
                \includegraphics[scale=0.3]{logo.png}
            \end{figure}

            \par \rule{\textwidth}{0.2pt}
            \par\Huge\textsc{TFDS Defect Detection - Self- and semi supervised leanring for industrial defect detection using MVTEC and VisA}%
            \par\rule[1ex]{\textwidth}{0.2pt}
            \par \large \color{black}%%		
            \large Tobias Schiele %
            
        \end{center}
        \vfill
    %
        \begin{flushright}\begin{minipage}{0.45\linewidth}
            \par\Large \color{black}
            % \par\large Proposal\\
            % \par\large Supervisor: \\ \large Dr. Prof. Ulrich Klauck\\
            % \par\large Examiner: \\ \large\@examinerB\\
            \par
        \end{minipage}\end{flushright}
        \vfill
    %
        \begin{center}
            \color{black}
            \vspace*{0mm}
            \small  Last updated : \MonthYearFormat\today
        \end{center}
    %
    \end{titlepage}
    
    \clearpage
    \pagenumbering{roman}

    %--- Abstract
    % \pagenumbering{Roman}
    % \hypertarget{abstract}{%
    \section*{Abstract} %\label{abstract}}
    
    %This work proposes a machine learning and computer vision platform.
    %As opposed to existing platforms, we focus on the developer instead of the end user.
    %Extending this platform is as simple as dropping in plain python modules. 
    %Thereby, anyone with limited python knowledge can make use of this project.
    
    %Additionally, this platform builds on streamlit.
    %This way, you can extend any of your scripts to a fully customizable app.
    
    %The main goal of this project is to enable rapid prototyping, reproducible workflows and collaboration.
    %The stakeholders of this project include computer scientists and researchers. 
    %To a certain degree, also end-users can be targeted. This depends on the usability of the apps you develop. 
    
    
    % \addcontentsline{toc}{section}{Abstarct}

    
    %--- Acknowledgements
    %\section*{Acknowledgments}


    %--- Affirmation
    %\section*{Affirmation}
    
    %Hereby I, Tobias Schiele, declare that I have conscientiously and independently 
    %written the present information in this thesis.

    %First, I assure you that I have not used any unspecified sources or auxiliary means. 
    %Second, all intellectual property of other authors is cited.
    %Third,  the present work is specially crafted for this thesis and has not been part of other projects.
    
    
    \tableofcontents
    %\listoffigures
    %\listoftables
    \clearpage
    \pagenumbering{arabic}

    % \RaggedRight
    
    """,

    # Sphinx Setup
    #
    'sphinxsetup': \
        'hmargin={0.75in,0.75in}, vmargin={1in,1in}, \
        verbatimwithframe=false, \
        inlineliteralwraps=true, \
        parsedliteralwraps=true, \
        TitleColor={rgb}{0.505,0.04,0.115}, \
        HeaderFamily=\\rmfamily\\bfseries, \
        InnerLinkColor={rgb}{0.1,0,0.5}, \
        OuterLinkColor={rgb}{0,0,0.2}, \
        VerbatimColor={rgb}{0.93,0.93,0.93}, \
        verbatimborder=0.1pt',

    # Table of contens
    # - defined in title
    #
    'tableofcontents':' ',

}
