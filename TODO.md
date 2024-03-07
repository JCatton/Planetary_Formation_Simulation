# Simulation
- ### Main Components
- [ ] Finish implementing basic hydrodynamics.
- [ ] Add gravity to the simulation.
- [ ] Generic initialisation function for proto-system particles.
  - Homogenous and isotropic large scale
  - Define random "clumping parameters"
  - [ ] Start with a star formed
- [ ] Exit conditions for simulation?
  - Number of time-steps.
  - Total time passed.
  - Body unmutability?
- ### Extension Work
- [ ] Thermal Pressure from a star?
- [ ] Thermal Pressure from a cooling planet?
  - Could be modelled just the same as a star?
- [ ] 3D
- [ ] Dynamic step size
- [ ] Particles act as different materials
  - This should enable planetary differentiation
    - Occurring mainly due to thermal pressure
  - Proto planetary Disc dynamics
    - Pressure gradients in disk 
    - Radial Migration 
    - Vertical Settling
- [ ] Magnetic Field Modelling
- ### Ancillary Systems

- [ ] Develop fast and easy to use system for writing data to a file.
  - Probably keep file for particle data completely separate to simulation data, and analysis will require reading of
both the simulation parameters and particle parameters and particle data.
  - [ ] Allow for loading of data using same system to initialise simulation.
- [ ] Parallelize code.
  - [ ] Make parallel code run on GPU.
---
# Data Analysis
### Simulation Tests
- Conservation Laws
  - [ ] Energy
    - We need to consider how this works with thermal pressure and cooling...
    - Due to Lagrangian based simulation not confined to grid --> Open system...
  - [ ] Angular Momentum
  - [ ] Mass
- Does it look right?
### Body Analysis
- [ ] How is a continuous body measured?
  - Define how we can read bodies as separate.
  - When should we ignore dust in large scale systems.
- [ ] System Density Cross-Sections
- [ ] System Composition Cross-Sections
### Visualisation
- [ ] Input data from simulation to make graphical representation.
- [ ] Animate time-series of simulation for all graphs.