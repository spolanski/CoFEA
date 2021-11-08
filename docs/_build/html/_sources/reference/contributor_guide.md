# Contributor Guide

Here is a quick introduction on how to start contributing to the CoFEA Initiative. At first, you can acknowledge yourself with the rules we try to follow:
- if you are not familiar with programming, compilation etc, we recommend using Ubuntu 18.0 (or any Debian based Linux) as your main environment. We tend to use this distribution and all guidelines presented in this docs have been validated with this OS.
- we use GitHub website as a place to store the code, docs and everything else. As a result of that, if you would like to contribute to CoFEA you should have an account on this platform to be able to fork the [CoFEA repository](https://github.com/spolanski/CoFEA), add your changes and send a modified version back. That also implies that you ought to have basic understanding of *git* version control system and the nomenclature used on GitHub (such as pull request, fork etc.)
- while it would be nice to use Python 3.x only, some FE codes (for example Salome) are still using Python version 2.7. Due to that, all scripts which are developed should be developed in a way that is more or less compatible with 2.x and 3.x versions.
- All the tasks we are currently working on are presented in the [CoFEA Github issues](https://github.com/spolanski/CoFEA/issues)
- While still not in place, please use snake_case for naming instead of camelCase rule or any different

## Documentation contribution

Your journey as a contributor should start with getting the copy CoFEA docs onto your hard-drive. It is actually very simple to recreate the website locally. You can do it by running following commands from terminal:

```bash
# Install python3.7 version; skip the step if you have it
sudo apt install python3.7
# Install virtualenv module for python3.7
python3.7 -m pip install virtualenv
# Download CoFEA repo
git clone https://github.com/spolanski/CoFEA.git
# open CoFEA folder
cd CoFEA/
# set up python virtualenv
python3.7 -m venv cofea_env
# activate the virtualenv
source cofea_env/bin/activate
# install all the modules which are required by CoFEA
python3.7 setup.py install
# go to docs folder
cd docs/
# execute sphinx to compile the website
make html
# open the local website in firefox
firefox _build/html/index
```

That's it! if you follow the steps above, you will compile the website locally. Then you can modify the files and send them back to the CoFEA github using git push command. We are looking forward to your contribution! 

:::{hint}
Looking for a task to do? Check [CoFEA documentation issue](https://github.com/spolanski/CoFEA/issues/27). It contains several things that we would like to implement. Pick one and [create a Github issue](https://github.com/spolanski/CoFEA/issues/new/choose), so everyone knows that someone is working on it. After that send a pull request and your work will be merged soon.
:::

## FE work contribution

Once the documentation works, you can set up the simulation environment. The CoFEA workflow currently used by contributors is following:
1. Salome_Meca 2019.3 is used to build/import geometries and meshes
2. Established model is tested in Code_Aster
3. Meshes are converted into format appropriate to run study in Calculix and Elmer
4. Optionally, the same setup is tested in different codes which are also free and open-source.

The best way way to contribute is to install Salome_Meca with Code_Aster, Calculix and Elmer, so that you could build your own models and contribute to the CoFEA initiative.

:::{hint}
Looking for a task to do? Check [FEA work issue](https://github.com/spolanski/CoFEA/issues/51). It contains several examples that we would like to test. Pick one and [create a Github issue](https://github.com/spolanski/CoFEA/issues/new/choose), so everyone knows that someone is working on it. After that send a pull request and your work will be merged soon.
:::

:::{important}
If you are an FE code developer and you would like to submit your own example or show results for already existing benchmark, feel free to add your contribution to the Benchmarks folder and send pull request.
:::


## Python scripts contribution

At the moment, the most work is done on the [Meshpresso Mesh Converter](../meshpresso/index.md). More information on how to contribute will be provided soon.
