# Tested Finite Element codes

## CalculiX
TODO

## Code_Aster

The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/08-C208_B_1_1_cantilever_beam/model_setup_CA)

### Note about boundaries used with Code_Aster
Load was imposed simultaneously increasingly by 5% on each step with one extra step corresponding to Nx = 489kN. The last one step corresponds to Nx=500kN

### Note about mesh used with Code_Aster
Mesh comprises of 2 order shell elements with  additional node inside. Other types of shell elements are unavailable to use with geometrical and material nonlinearities.

### Run model in Code_Aster in a few steps:  
1. Run B_1_1_cantilever_beam.py in python to generate mesh - med by default.
2. Change paths in *.astk files to your own, and also optionally change 'current_path' variable in B_1_1_cantilever_beam_calculation.comm
3. Run B_1_1_cantilever_beam_calculation.astk
4. Replace into True requested output field
5. Run B_1_1_cantilever_beam_postpro.astk
6. Enjoy received .rmed or .resu files

## Elmer
TODO
