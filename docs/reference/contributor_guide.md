# Contributor Guide

Here is a quick introduction on how to start contributing to the CoFEA Initiative. At first, you can acknowledge yourself with rules we try to follow and which we also recommend:
- if you are not familiar with programming, compilation etc, we recommend using Ubuntu 18.0 (or any Debian based Linux) as your main environment. We tend to use this distribution and all guidelines presented in this docs have been validated with this OS.
- we use GitHub website as a place to store the code, docs and everything else. As a result of that, if you would like to contribute to CoFEA you should have an account on this platform to be able to fork the [CoFEA repository](https://github.com/spolanski/CoFEA), add your changes and send a modified version back. That also implies that you ought to have basic understanding of *git* version control system and the nomenclature used on GitHub (such as pull request, fork etc.)
- while it would be nice to use Python 3.x only, some FE codes (for example Salome) are still using Python version 2.7. Due to that, all scripts which are developed should be developed in a way that is more or less compatible with 2.x and 3.x versions.
- All the tasks we are currently working on are presented in the [CoFEA Github issues](https://github.com/spolanski/CoFEA/issues)
- While still not in place, please use snake_case for naming instead of camelCase rule or any different

## Documentation contribution

Your journey as a contributor should start with getting the copy CoFEA onto your hard-drive. You can do it by clicking the [download link](https://github.com/spolanski/CoFEA/archive/master.zip) or by running *git clone https://github.com/spolanski/CoFEA.git* command if you are using git.

CoFEA uses [Sphinx Book Theme](https://sphinx-book-theme.readthedocs.io/en/latest/index.html) to automatically create this website. So the next step will be to to install Sphinx and some additional prerequisites. In this instruction it will be shown how to do that and covert the *.md files into html ones.

### Sphinx prerequisites

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

### Building html website from .MD files

Navigate to github CoFEA/docs directory in your terminal, then simply type:

```
make html
```

After this command Sphinx will automatically convert Markdown files into HTML. If you are curious how they look like, open the file from docs/_build/html/index.html in your web browser. You should see the local copy of this webpage.

Once you add some modifications, you can send a pull request. Once accepted, the .md files will be converted and the conversion status can be seen on the [Read the Docs](https://readthedocs.org/projects/cofea/builds/) page.

:::{hint}
Looking for a task to do? Check [CoFEA documentation tasks issue](https://github.com/spolanski/CoFEA/issues/27)
:::

## FE work contribution

Once the documentation works, you can set up the simulation environment. The CoFEA workflow currently used by contributors is following:
1. Salome_Meca 2019.3 is used to build/import geometries and meshes
2. Established model is tested in Code_Aster
3. Meshes are converted into format appropriate to run study in Calculix and Elmer
4. Optionally, the same setup is tested in different codes which are also free and open-source.

The best way way to contribute is to install Salome_Meca with Code_Aster, Calculix and Elmer, so that you could build your own models and contribute to the CoFEA initiative.

:::{important}
If you are developing your own FE-code or know how to use different free and open-source simulation environment, feel free to it to the Benchmarks folder and send pull request. You can send already existing benchmark with results from different code or something totally new.
:::

:::{hint}
Looking for a task to do? Check [FEA work issue](https://github.com/spolanski/CoFEA/issues/51)
:::

## Python scripts contribution

At the moment, the most work is done on the [Meshpresso Mesh Converter](../meshpresso/index.md). More information on how to contribute will be provided soon.