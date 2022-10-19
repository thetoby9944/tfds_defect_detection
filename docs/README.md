# Sphinx Documentation

The documentation is standard sphinx documentation. 
Detailed descriptions on the specific sphinx setup can be found
in `/doc/conf.py` (the sphinx configuration document). 

Make sure all requirements from `doc/requirements.txt` are installed
    
    pip install -r requirements.txt

### Hosting

Host this sphinx-documentation server by changing into the `doc` folder. There run:

    sphinx-autobuild --host 0.0.0.0 --port 8800 . _build

### Building

This server will be continuously running and looking for changes in the .rst files.
If any changes do not take effect, generate the documentation from scratch.
To generate the documentation from scratch, delete all auto-generated code in

    rm -rf _build
    rm -rf autoapi
    
Then rerun the `sphinx-autobuild` command

#### HTML

To generate the plain HTML output run

    make html

### Latex

Some attempt has been made to create decent latex documentation from sphinx. 
But if possible, avoid reading the latex documentation for the Reference API 
(generated from docstrings).
Instead, read the online documentation or HTML version or use a code explorer-like
PyCharm or Visual Studio Code to directly navigate the code and the docstrings.

To build the latex document plus the resulting .pdf file simply run

    make latexpdf
    
Make sure the lualatex engine is installed. 
Otherwise, change the `latex_engine` variable in `doc/conf.py`.

Ignore any errors if possible, otherwise, check if all package versions are up to date.
If any cross-references or figures do not show up, rerun multiple times.

### Documentation Process

The documentation consists of primarily simple markdown files 
and `index.rst` files which glue these together to chapters.

On the root level of the documentation `/doc`, the sphinx root `index.rst` 
glues the chapters together.

#### Documentation from docstrings

The library `sphinx-autoapi` generates additional reference API documentation from docstrings
which are written in `.rst` style syntax.

#### Flask endpoints / REST Interface

With the sphinx extension `sphinxcontrib.autohttp.flask` the flask endpoints are documented from docstrings.

#### Markdown vs. reStructuredText

If the markdown syntax at some point proves insufficient for a section, the tool [cloudconverter](https://cloudconvert.com/md-converter) has been used.
This tool allows us to convert the markdown document to reStructuredText.
Now, elements like 

- multiline tables, 
- bibtex-citations and 
- referencable named / numbered figures 

can be used.



#### The bibliography

The bibliography has been build with sphinx by

1. Bookmarking every important page which has been visited during development
1. Exporting the bookmarks to HTML via the browser.
1. Converting the HTML bookmarks including the folder structure to markdown with sections
1. Clicking through the links and generating BibTeX entries with [BibItNow](https://chrome.google.com/webstore/detail/bibitnow/bmnfikjlonhkoojjfddnlbinkkapmldg/related) and save in `ref.bib`.
1. Pasting `:cite:` .rst-commands for the Bibtex entries where needed.
1. Include a `.. bibliography: ref.bib` directive.

Of course, for instead of bookmarking, tools like Mendeley and Citavi exist, but they are yet another tool which has to be 
managed and slows down documenting.

Generating the references from the bookmarks folder structure has the additional advantage to provide a full markdown scaffold for the literature review section.
With this process, orderly bookmarking your references write half a literature review for you automatically.   
