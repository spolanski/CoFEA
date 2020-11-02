sphinx-apidoc -o ./docs . [*main*,] -f --no-toc 
cd docs
make html
cd ..
