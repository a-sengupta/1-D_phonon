# 1-D_phonon
LAMMPS simulation of phonon through 1D atomic chain

The base version which this repository will start from are the files that were made on the 17th of July, 2017. The basic setup is as follows:
- There are 2 atom types; they differ only in label (and position) but are identical in other respects.
- Atoms of the same type are *bonded* to each other harmonically.
- Atoms of different types interact via a *pairwise* Lennard-Jones potential.
- The type-1 group of atoms consists of 8 atoms, numbered 1-8, in a 1D chain placed 1 LJ unit of distance apart. The same is true for the type-2 atoms, except the atoms are labelled 9-16.
- The two chains, or rather, atoms 8 and 9 are spaced 3 LJ units of distance apart from each other.
