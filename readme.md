# Vehicle Use Phase Energy Calculator (VUPEC)
Author:Duncan Kushnir (dk at duncankushnir point com)

VUPEC is a calculator for the use phase energy a vehicle consumes while driving.  

Initial development has been funded by energimydigheten.se as part of the ERA-NET cofund program
 alongside the proEME consortium (proEME.eu) for EU Horizon2020. 

The model is still under intensive development.  Contact the author if there are any questions or
 if you want capabilities included. 
 
Link to latest description report: 
www.duncankushnir.net/doc-vupec.pdf

## Purpose
To provide an accurate and modifiable model for calculating the energy requirements of vehicles. 

## Scope
From first physics principles through to energy inputs to the vehicle (petrol, natural_gas
, electricity at plug, etc.)

## Features
- All relevant drive cycles included as well as parsing engine.. paint your own!
- Accurate physics, even with altitude and temperature corrections
- Fully separate import engine for vehicles and components
- Calculates standard driving cycle energy use to within 5% of reported - all vehicle makes, all
 drive cycles
 - graph friendly result dumping
 - web based GUI
 
## Get Started
- Clone the directory
- run setup.bat or setup.sh to set up a virtual env (depending on win/linux)
- run.bat or run.sh
- navigate a web browser to http://127.0.0.1

## Or test a live version
www.duncankushnir.net/vupec

## Future
Current development priorities
- GUI state glitch
- GUI present 'advanced mode'
- AC induction motor model
- Final database specification 
