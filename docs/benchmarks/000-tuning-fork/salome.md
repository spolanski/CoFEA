# Code_Aster

Unfortunately Code_Aster isn't ideal solver to obtain frequencies which are almost zero therefore the option BANDE was used to calculate frequencies in certain bandwidth. Below there is an explanation of the input file of Code_Aster.

```
DEBUT()


mesh = LIRE_MAILLAGE(FORMAT='MED',                          # Read the mesh
                     UNITE=20,
                     VERI_MAIL=_F())

model = AFFE_MODELE(AFFE=_F(MODELISATION=('3D', ),          # Assigning the element to the model
                            PHENOMENE='MECANIQUE',
                            TOUT='OUI'),
                    MAILLAGE=mesh)

mater = DEFI_MATERIAU(ELAS=_F(E=207000.0,                   # Defining the material
                              NU=0.33,
                              RHO=7.829e-09))

fieldmat = AFFE_MATERIAU(AFFE=_F(MATER=(mater, ),           # Assigning the material to the mesh
                                 TOUT='OUI'),
                         MAILLAGE=mesh,
                         MODELE=model)

ASSEMBLAGE(CHAM_MATER=fieldmat,                             # Setting the right matrixes for simulation
           MATR_ASSE=(_F(MATRICE=CO('MASS'),
                         OPTION='MASS_MECA'),
                      _F(MATRICE=CO('RIGI'),
                         OPTION='RIGI_MECA')),
           MODELE=model,
           NUME_DDL=CO('ndl'))




modes = CALC_MODES(CALC_FREQ=_F(FREQ=(100.0, 3000.0)),      # Setting the solver BANDE option between 100 and 3000 Hz.
                   MATR_MASS=MASS,
                   MATR_RIGI=RIGI,
                   OPTION='BANDE',
                   SOLVEUR_MODAL=_F(METHODE='TRI_DIAG',
                                    ),
                   TYPE_RESU='DYNAMIQUE')


IMPR_RESU(FORMAT='MED',                                     # Saving the result in 3D format
          RESU=_F(INFO_MAILLAGE='OUI',
                  RESULTAT=modes),
          UNITE=80)

IMPR_RESU(FORMAT='RESULTAT',                                # Saving the result in .dat file
          RESU=_F(RESULTAT=modes),
          UNITE=8)


FIN()

```
The simulation input file used in this study can be found on our [GitHub](https://github.com/spolanski/CoFEA/tree/master/Benchmarks/00-Tuning-Fork/MODEL_Code_Aster)!
