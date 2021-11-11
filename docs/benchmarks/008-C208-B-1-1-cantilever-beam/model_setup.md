# Model setup

## Model definition

Freely available standard " DNV-RP-C208 Determination of Structural Capacity by Non-linear FE analysis Methods 2013"* published by Det Norske Verites AS describes methodologies of structural assessment in oil&gas industry. The standard includes a few FEM examples concerning mechanisms of failure available for assessment only with taking into account nonlinear phenomena. Original examples are solved using Abaqus.

'*'Source:
[1] - https://rules.dnv.com/docs/pdf/DNVPM/codes/docs/2013-06/RP-C208.pdf  

First example is describing simple cantilever beam with specific way to assess its ultimate load taking into account nonlinear behaviour of material and geometrical nonlinearities.

### Essential dimensions
The geometry consists of one cantilever prismatic T-beam:
```{figure} . /files_model_setup/B_1_1_geometry_and_boundary_conditions.png
---
width: 600px
alt: C208 Cantilever Beam
name: C208 Cantilever Beam - essential dimension, boundaries and load abbreviations (Source of the picture - [1]).
---
C208 Cantilever Beam - essential dimension, boundaries and load abbreviations (Source of the picture - [1]).
```

```{jupyter-execute}
:hide-code:
  from ipygany import Scene, TetraMesh
  mesh = TetraMesh.from_vtk(r'benchmarks/008-C208-B-1-1-cantilever-beam/files_model_setup/cantilever_beam.vtk')
  scene = Scene([mesh])
  scene
```

```{Tip}
The cantilever geometry shown above is interactive
```

### Centroid assessment
Model description in [1] lacks of section center height.
Center coordinates of the area shall be calculated based on first moments of rectangles.

Subscript 'v' stands for 'vertical plate' - flange  
Subscript 'h' stands for 'horizontal plate' - web

Cross section areas:  
A<sub>v</sub> = 8 mm * 460 mm = 3680 mm<sup>2</sup>   
A<sub>h</sub> = 40 mm * 300 mm = 12000 mm<sup>2</sup>

First moment of areas acc. to gravity center of horizontal plate:  
S<sub>v</sub> = A<sub>v</sub> * (460/2 + 40/2) = 920e3 mm<sup>3</sup>      
S<sub>h</sub> = 0 mm<sup>3</sup>

Centroid of cross section area is yc above symmetry line of vertical plate:  
yc = (S<sub>v</sub> + S<sub>h</sub>) / (A<sub>v</sub> + A<sub>h</sub>) = 920e3 mm<sup>3</sup> / 15680 mm<sup>2</sup> = 58.67 mm

```{figure} . /files_model_setup/B_1_1_sketch_centroid.png
---
width: 200px
alt: C208 Cantilever Beam
name: C208 Cantilever Beam - centroid center calculation.
---
C208 Cantilever Beam - centroid center calculation.
```

## Target solution

Chief point is comparison of plastic strain obtained with various FEM codes through height of section with data given in standard [1]. Chosen failure line is third row of elements from restraint side.

```{figure} . /files_model_setup/B_1_1_plasticity_aim_profile.png
---
width: 400px
alt: C208 Cantilever Beam
name: C208 Cantilever Beam - benchmark results (Source of the picture - [1]).
---
C208 Cantilever Beam - benchmark results (Source of the picture - [1]).
```

Plastic strain benchmark curve was digitized with picture digitizer.

```{figure} . /files_model_setup/B_1_1_plasticity_aim_profile_digitized.png
---
width: 400px
alt: C208 Cantilever Beam
name: C208 Cantilever Beam - digitized values based on figure.
---
C208 Cantilever Beam - digitized values based on figure.
```

'*'[2] - http://plotdigitizer.sourceforge.net/

## Material properties

Beam plates are modeled as plastic piece-wise linear S355 acc. to [1] s.4.7.5. using true or engineering stress-strain curve (standard doesn't definite this matter unambiguously) - both possibilities have been taken into consideration.
Vertical and horizontal plates have relevantly various thicknesses, what shall be taken into account.  
Material is ideally plastic in range above material tensile strength.
```{figure} . /files_model_setup/B_1_1_material_definition.png
---
width: 800px
alt: C208 Cantilever Beam
name: C208 Cantilever Beam_
---
C208 Cantilever Beam - piece-wise material definitions related to thickness and type of curve.
```
### Material definition based on true stress-strain
Values to implement in material definition for 16mm thickness S355:  
|Strain| 	 Stress [MPa]  |
|------|----------------|
|0.0000| 	 0            |
|0.0015| 	 320          |
|0.0055| 	 357          |
|0.0212| 	 366          |
|0.1406| 	 541          |
|0.2797| 	 541          |

Values to implement in material definition for 16-40 mm   thickness S355:  
|Strain| 	 Stress [MPa]  |
|------|----------------|
|0.0000| 	 0            |
|0.0015| 	 311          |
|0.0055| 	 346.9        |  
|0.0212| 	 355.9        |
|0.1406| 	 541.6        |
|0.2797| 	 541.6        |

### Material definition based on engineering stress-strain:
Values to implement in material definition for 16mm thickness S355:  
|Strain| 	 Stress [MPa]  |
|------|----------------|
|0.0000| 	 0            |
|0.0015| 	 319.5        |
|0.0055| 	 355          |
|0.0215| 	 358.4        |
|0.1515| 	 470          |
|0.3015| 	 470          |

Values to implement in material definition for 16-40 mm thickness S355:  
|Strain| 	 Stress [MPa]  |
|------|----------------|
|0.0000|	 0            |
|0.0015| 	 310.5        |
|0.0055| 	 345          |
|0.0215| 	 348.4        |
|0.1515| 	 470          |
|0.3015| 	 470          |

## Boundary conditions

Nx = 500 kN  
P = -0.15 * Nx   
M = -0.45 * Nx * 1m  

On 'restraint' group of nodes lack of displacement in each direction is imposed.
On 'force' group of nodes are imposed loads N, P, M indirectly by auxiliary point placed in the center of cross section centroid - additional kinematic relations are necessary.

```{figure} . /files_model_setup/B_1_1_boundaries.png
---
width: 600px
alt: C208 Cantilever Beam
name: C208 Cantilever Beam - boundaries.
---
C208 Cantilever Beam - boundaries.
```

Geometrical nonlinearity shall be taken into account, because significant angles of rotation are expected.


## Mesh

Mesh is created approximately with mesh size 16mmx16mm using gmsh.
Original example described in [1] uses I order elements.

Mesh contains also auxiliary point named 'aux_point' - point indirectly through MPC exerts moment and forces into 'force' group of nodes.

```{figure} . /files_model_setup/B_1_1_mesh.png
---
width: 600px
alt: C208 Cantilever Beam
name: C208 Cantilever Beam - mesh.
---
C208 Cantilever Beam - mesh.
```
