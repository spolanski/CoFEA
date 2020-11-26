# Sphinx
To use Sphinx and create documentation you must install some prerequisities first. In this instruction it will be shown how to do that and covert the *.md files into html ones.

## Tools
1. Install the required tools for Sphinx:
    - jinja2,
    - pyyaml,
    - docutils>=0.15,
    - sphinx,
    - click,
    - pydata-sphinx-theme~=0.4.1,
    - beautifulsoup4,
    - importlib-resources~=3.0.0; python_version < 3.7,
    - myst-nb,
    - sphinx-copybutton,
    - sphinx-togglebutton,
    - sphinxcontrib-bibtex,
    - sphinx-thebe,
    - ablog,
    - sphinx-book-theme,

using your python package manager. For Ubuntu and Debian-oriented system the command can be like:

```
pip3 install jinja2
```

or if you are using anaconda just type:

```
conda install -c anaconda jinja2
```

## Converting *.md into html files

Navigate to github CoFEA/docs directory in your terminal, then simply type:

```
make html
```

After this command Sphinx will automatically convert Markdown files into HTML. After this operation just push them to the repository. The changes done in a documentation structure will be visible shortly after uploading files into Github.
