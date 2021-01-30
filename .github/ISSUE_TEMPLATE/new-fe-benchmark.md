---
name: New FE benchmark
about: This issue is used when a new FE model is going to be tested
title: ''
labels: benchmark
assignees: ''

---

# New benchmark issue template
## Report related tasks
- [ ] Create a folder directory in **benchmarks** folder on CoFEA Github
- [ ] Write a Readme file which contains:
  - [ ] Benchmark purpose - describe what the benchmark is trying to measure
  - [ ] Model sketch - prepare a sketch with dimensions or provide any useful image
  - [ ] Material - write down material data
  - [ ] Boundary conditions and loads - describe boundary conditions and loads
  - [ ] Mesh - describe topology of mesh used in the study
## FE study related tasks
- [ ] setup model in Salome-Meca
- [ ] run benchmark in Code_Aster
- [ ] run benchmark in Calculix
- [ ] run in any different code
- [ ] extract the results of interest and add them to readme file
