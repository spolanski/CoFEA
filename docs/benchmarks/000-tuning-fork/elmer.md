# Elmer

Elmer supports rigid body modes out of the box. Below there is an explanation of solver input file.

```
Header
  CHECK KEYWORDS Warn
  Mesh DB "." "Mesh/QUAD-HEX-0-5" # Path to the mesh
  Include Path ""
  Results Directory "Results"     # Path to results directory
End

Simulation                        # Settings and constants for simulation
  Max Output Level = 5
  Coordinate System = Cartesian
  Coordinate Mapping(3) = 1 2 3
  Simulation Type = Steady state
  Steady State Max Iterations = 1
  Output Intervals = 1
  Timestepping Method = BDF
  BDF Order = 1
  Solver Input File = case.sif
  Post File = case.ep
End

Constants                          
  Gravity(4) = 0 -1 0 9.82
  Stefan Boltzmann = 5.67e-08
  Permittivity of Vacuum = 8.8542e-12
  Boltzmann Constant = 1.3807e-23
  Unit Charge = 1.602e-19
End

Body 1                            # Assigning the material and equations to the mesh
  Target Bodies(1) = 1
  Name = "Body 1"
  Equation = 1
  Material = 1
End

Solver 1                          # Solver settings
  Equation = Linear elasticity
  Procedure = "StressSolve" "StressSolver"
  Eigen System Select = Smallest magnitude
  Eigen System Values = 10
  Variable = -dofs 3 Displacement
  Eigen Analysis = True
  Exec Solver = Always
  Stabilize = True
  Bubbles = False
  Lumped Mass Matrix = False
  Optimize Bandwidth = True
  Linear System Convergence Tolerance = 1.0e-3
  Steady State Convergence Tolerance = 1.0e-5
  Nonlinear System Convergence Tolerance = 1.0e-7
  Nonlinear System Max Iterations = 1
  Nonlinear System Newton After Iterations = 3
  Nonlinear System Newton After Tolerance = 1.0e-3
  Nonlinear System Relaxation Factor = 1
  Linear System Solver = Direct
  Linear System Direct Method = MUMPS
End

Solver 2                          # Extracting the result to the .dat file
  Exec Solver = After Saving
  Equation ="Equation 1"
  Procedure = "SaveData" "SaveScalars"
  Filename = "QUAD-HEX-0-5.dat"
  Variable 1 = Displacement
  Save Eigenfrequencies = Logical True
End

Equation 1                        # Setting the active solvers
  Name = "Equation 1"
  Active Solvers(2) = 1 2
End

Material 1                        # Defining the material
  Name = "Steel"
  Mesh Poisson ratio = 0.33
  Youngs modulus = 207000
  Poisson ratio = 0.33
  Porosity Model = Always saturated
  Density = 7.829e-9
End

```


The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/benchmarks/00-Tuning-Fork/MODEL_ElmerGUI)!
