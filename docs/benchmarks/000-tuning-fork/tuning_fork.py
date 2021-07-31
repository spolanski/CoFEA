"""

"""
###############################################################################

import time
import getfem as gf
import numpy as np
import scipy
from scipy import io
from scipy.sparse import linalg

###############################################################################
# Let us now define the different physical and numerical parameters of the problem.
#

rho = 7.829e-09  # Young Modulus (kg/mm^3)
E = 207000  # Young Modulus (N/mm^2)
nu = 0.33  # Poisson ratio
clambda = E * nu / ((1 + nu) * (1 - 2 * nu))  # First Lame coefficient (N/mm^2)
cmu = E / (2 * (1 + nu))  # Second Lame coefficient (N/mm^2)

###############################################################################
# Set the numerical parameter of each case.
#

elements_degrees = []
msh_file_names = []

# Linear-Tet 2.0mm
elements_degrees.append(1)
msh_file_names.append("./LIN-TET/TET-2-0.msh")

# Linear-Tet 1.0mm
elements_degrees.append(1)
msh_file_names.append("./LIN-TET/TET-1-0.msh")

# Linear-Tet 0.5mm
elements_degrees.append(1)
msh_file_names.append("./LIN-TET/TET-0-5.msh")

# Quad-Tet 2.0mm
elements_degrees.append(2)
msh_file_names.append("./LIN-TET/TET-2-0.msh")

# Quad-Tet 1.0mm
elements_degrees.append(2)
msh_file_names.append("./LIN-TET/TET-1-0.msh")

# Quad-Tet 0.5mm
elements_degrees.append(2)
msh_file_names.append("./LIN-TET/TET-0-5.msh")

# Linear-Hex 2.0mm
elements_degrees.append(1)
msh_file_names.append("./LIN-HEX/HEX-2-0.msh")

# Linear-Hex 1.0mm
elements_degrees.append(1)
msh_file_names.append("./LIN-HEX/HEX-1-0.msh")

# Linear-Hex 0.5mm
elements_degrees.append(1)
msh_file_names.append("./LIN-HEX/HEX-0-5.msh")

# Quad-Hex 2.0mm
elements_degrees.append(2)
msh_file_names.append("./LIN-HEX/HEX-2-0.msh")

# Quad-Hex 1.0mm
elements_degrees.append(2)
msh_file_names.append("./LIN-HEX/HEX-1-0.msh")

# Quad-Hex 0.5mm
elements_degrees.append(2)
msh_file_names.append("./LIN-HEX/HEX-0-5.msh")

t = time.process_time()

###############################################################################
# Importing the mesh from gmsh format.
#

meshs = []

for i, msh_file_name in enumerate(msh_file_names):
    mesh = gf.Mesh("import", "gmsh", msh_file_name)
    meshs.append(mesh)

print("Time for import mesh", time.process_time() - t)
t = time.process_time()

###############################################################################
# Definition of finite elements methods and integration method
#

mfus = []
mfds = []
mims = []

for elements_degree, mesh in zip(elements_degrees, meshs):

    mfu = gf.MeshFem(mesh, 3)
    mfu.set_classical_fem(elements_degree)
    mfus.append(mfu)

    mfd = gf.MeshFem(mesh, 1)
    mfd.set_classical_fem(elements_degree)
    mfds.append(mfd)

    mim = gf.MeshIm(mesh, elements_degree * 2)
    mims.append(mim)

###############################################################################
# We get the mass and stiffness matrices using asm function.
#

mass_matrixs = []
linear_elasticitys = []

for i, (mfu, mfd, mim) in enumerate(zip(mfus, mfds, mims)):

    mass_matrix = gf.asm_mass_matrix(mim, mfu, mfu)
    mass_matrix.scale(rho)
    mass_matrixs.append(mass_matrix)

    lambda_d = np.repeat(clambda, mfd.nbdof())
    mu_d = np.repeat(cmu, mfd.nbdof())
    linear_elasticity = gf.asm_linear_elasticity(mim, mfu, mfd, lambda_d, mu_d)
    linear_elasticitys.append(linear_elasticity)

    mass_matrix.save("hb", "M" + "{:02}".format(i) + ".hb")
    linear_elasticity.save("hb", "K" + "{:02}".format(i) + ".hb")

print("Time for assemble matrix", time.process_time() - t)
t = time.process_time()

###############################################################################
# Solve the eigenproblem.
#
# Compute the residual error for SciPy.
#
# :math:`Err=\frac{||(K-\lambda.M).\phi||_2}{||K.\phi||_2}`
#
# Convert Lambda values to Frequency values:
# :math:`freq = \frac{\sqrt(\lambda)}{2.\pi}`
#

for i, (mass_matrix, linear_elasticity, mfu) in enumerate(
    zip(mass_matrixs, linear_elasticitys, mfus)
):

    M = io.hb_read("M" + "{:02}".format(i) + ".hb")
    K = io.hb_read("K" + "{:02}".format(i) + ".hb")
    vals, vecs = linalg.eigsh(A=K, k=6, M=M, sigma=400.0, which="LA")

    omegas = np.sqrt(np.abs(vals))
    freqs = omegas / (2.0 * np.pi)

    nev = 6

    scipy_acc = np.zeros(nev)

    print(f"case{i}")

    for j in range(nev):
        lam = vals[j]  # j-th eigenvalue
        phi = vecs.T[j]  # j-th eigenshape

        kphi = K * phi.T  # K.Phi
        mphi = M * phi.T  # M.Phi

        kphi_nrm = np.linalg.norm(kphi, 2)  # Normalization scalar value

        mphi *= lam  # (K-\lambda.M).Phi
        kphi -= mphi

        scipy_acc[j] = np.linalg.norm(kphi, 2) / kphi_nrm  # compute the residual
        print(f"[{j}] : Freq = {freqs[j]:8.2f} Hz\t Residual = {scipy_acc[j]:.5}")

    np.savetxt("freqs" + "{:0=3}".format(i) + ".txt", freqs)
    mfu.export_to_vtk(
        "vecs" + "{:0=3}".format(i) + ".vtk",
        mfu,
        vecs[:, 0],
        "Mode_1",
        mfu,
        vecs[:, 1],
        "Mode_2",
        mfu,
        vecs[:, 2],
        "Mode_3",
        mfu,
        vecs[:, 3],
        "Mode_4",
        mfu,
        vecs[:, 4],
        "Mode_5",
        mfu,
        vecs[:, 5],
        "Mode_6",
    )

print("Time for solve eigen value problem", time.process_time() - t)
t = time.process_time()
