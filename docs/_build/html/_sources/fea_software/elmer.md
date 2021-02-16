# Elmer

## Setup and compilation from source
Instalation process of ElmerGUI is straightforward. It is needed to add Elmer sources and then just download the package. To do so please use following commands:


```
sudo apt-add-repository ppa:elmer-csc-ubuntu/elmer-csc-ppa
sudo apt-get update
sudo apt-get install elmerfem-csc-eg
```

## How  to use ElmerGUI with Benchmarks

Please start ElmerGUI with:


```
ElmerGUI
```
Please load .unv mesh with Open File icon, then generate .sif file (Ctrl+G) and save the project. Then replace the generated .sif and .xml files with ones uploaded on CoFEA github. Start ElmerGUI and click import project and navigate to the project directory and click open. The benchmarking files should import without troubles.
