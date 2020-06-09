# Multiagent Table Analysis
A rough computational approach to picking the best seat.

## Data

A seat is defined by the 3-tuple (X,Y,Theta), denoting the position and direction the seat faces.
The X,Y coordinates are in units of imperial feet, roughly. The positive X axis points right, positive Y axis points up. Theta is in degrees, with 0 degrees pointing right. 


A table is defined by a set of seats. The area of the table is approximated as the amount of space enclosed by the convex hull of each seat, but will later be more specifically simulated.

## Model

Each seat can contain, at most, one person.

Each person has a viewcone that describes how well they can engage/interact with another person. The shape, roughly determined by the field of view and density of retinal receptors, is as follows:

[insert viewcone shape]

This emulates how well an individual can focus on another at any given angle and position. The density of retinal cells follows:

<img src="retinal_density.jpg"/>

The depth of field also decays according to:

<img src="https://latex.codecogs.com/gif.latex?d_f = max(2,5-dist)" /> 



In addition, the viewcone decays by factor lambda as an individual rotates left or right by gamma degrees according to the following equation:
<img src="https://latex.codecogs.com/gif.latex?\lambda = (90/(1-\alpha)-abs(\gamma))/90/(1-\alpha)" /> 
