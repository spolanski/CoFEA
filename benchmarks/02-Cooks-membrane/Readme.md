# Cook's membrane - linear version
![image](./combbase.png)
![image](./image-1.jpg)

## Material
Linear elastic material model:
- Young's modulus: 70.0 MPa
- Poisson's ratio: 1/3 and 0.499995
## Boundary conditions
- Fixed at one side
- Z-symmetry condition on both front faces Uz=0 (for solid elements only; no need for plain strain)
## Loading
- Shear load applied to face 6.25 N/mm^2
## Benchmark purpose
The purpose of the benchmark is to:
- find out if code can apply shear load to the face
- check if vertical displacement of point A is somewhere close to 32.00 mm for Poisson's ratio 1/3 and 28.8 mm for Poisson's ratio 0.499995
## Mesh files
Mesh files are available in the benchmark directory

[lowpoiss](./lowpoiss.png)
[highpoiss](./highpoiss.png)


More about the study can be found in the [link](http://www.simplassoftware.com/benchmarks.html#fig:Basic-verification-tests)
