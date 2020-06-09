

# Multiagent Table Analysis
A rough computational approach to picking the best seat.

## Data

A seat is defined by the 3-tuple (X,Y,Theta), denoting the position and direction the seat faces.
The X,Y coordinates are in units of imperial feet, roughly. The positive X axis points right, positive Y axis points up. Theta is in degrees, with 0 degrees pointing right. 


A table is defined by a set of seats. The area of the table is approximated as the amount of space enclosed by the convex hull of each seat, but will later be more specifically simulated.

## Model

Each seat can contain, at most, one person.

The depth of field decays according to:

![\lambda_{dof} = max(2,5-\sqrt{(x_{p_o}-x_{p_s})^2+(y_{p_o}-y_{p_s})^2})](https://render.githubusercontent.com/render/math?math=%5Clambda_%7Bdof%7D%20%3D%20max(2%2C5-%5Csqrt%7B(x_%7Bp_o%7D-x_%7Bp_s%7D)%5E2%2B(y_%7Bp_o%7D-y_%7Bp_s%7D)%5E2%7D))

In addition, the viewcone decays as an individual rotates left or right by ![\gamma](https://render.githubusercontent.com/render/math?math=%5Cgamma) degrees according to the following equation. Alpha denotes the fraction of engagement a fully lateral interaction would have compared to a frontal interaction:
![\lambda_{rot} = (90/(1-\alpha)-abs(\gamma))/(90/(1-\alpha))](https://render.githubusercontent.com/render/math?math=%5Clambda_%7Brot%7D%20%3D%20(90%2F(1-%5Calpha)-abs(%5Cgamma))%2F(90%2F(1-%5Calpha)))

We know the angle of incidence, that is, the angle of p_o in p_s's field of view, is:

![\gamma = \arctan(\abs(\frac{(\abs(x_{p_o}-x_{p_s}) * \sin(90-\theta_{p_s}) + \abs(y_{p_o}-y_{p_s}) * \cos(90-\theta_{p_s}))}{\abs(x_{p_o}-x_{p_s}) * \cos(90-\theta_{p_s}) - \abs(y_{p_o}-y_{p_s}) * \sin(90-\theta_{p_s})}))](https://render.githubusercontent.com/render/math?math=%5Cgamma%20%3D%20%5Carctan(%5Cabs(%5Cfrac%7B(%5Cabs(x_%7Bp_o%7D-x_%7Bp_s%7D)%20*%20%5Csin(90-%5Ctheta_%7Bp_s%7D)%20%2B%20%5Cabs(y_%7Bp_o%7D-y_%7Bp_s%7D)%20*%20%5Ccos(90-%5Ctheta_%7Bp_s%7D))%7D%7B%5Cabs(x_%7Bp_o%7D-x_%7Bp_s%7D)%20*%20%5Ccos(90-%5Ctheta_%7Bp_s%7D)%20-%20%5Cabs(y_%7Bp_o%7D-y_%7Bp_s%7D)%20*%20%5Csin(90-%5Ctheta_%7Bp_s%7D)%7D)))

This emulates how well an individual can focus on another at any given angle and position. The density of retinal cells follows:

<img src="https://raw.githubusercontent.com/Suhas7/mas-tables/master/retinal_densities.jpg"/>

We also simulate that, for any particular person (p_o) in your (p_s) field of view, the angle of incidence impacts engagement.

![\lambda_{eng} = 1 - \mod(\theta_{p_o}-\theta_{p_s}+180, 360)/180](https://render.githubusercontent.com/render/math?math=%5Clambda_%7Beng%7D%20%3D%201%20-%20%5Cmod(%5Ctheta_%7Bp_o%7D-%5Ctheta_%7Bp_s%7D%2B180%2C%20360)%2F180)

Given that the person is facing a direction, ![\theta](https://render.githubusercontent.com/render/math?math=%5Ctheta), their view of a particular point is proportional to the following, equivalent, formulas:

![\f(p_s,p_o)=\lambda_{dof}*\lambda_{rot}*\lambda_{eng}](https://render.githubusercontent.com/render/math?math=%5Cf(p_s%2Cp_o)%3D%5Clambda_%7Bdof%7D*%5Clambda_%7Brot%7D*%5Clambda_%7Beng%7D)

![\f(p_s,p_o)=max(2,5-\sqrt{(x_{p_o}-x_{p_s})^2+(y_{p_o}-y_{p_s})^2}) * ((90/(1-\alpha)-abs(\gamma))/(90/(1-\alpha))) * (1 - \mod((\theta_{p_o},360-\theta_{p_s}+180, 360))/180)](https://render.githubusercontent.com/render/math?math=%5Cf(p_s%2Cp_o)%3Dmax(2%2C5-%5Csqrt%7B(x_%7Bp_o%7D-x_%7Bp_s%7D)%5E2%2B(y_%7Bp_o%7D-y_%7Bp_s%7D)%5E2%7D)%20*%20((90%2F(1-%5Calpha)-abs(%5Cgamma))%2F(90%2F(1-%5Calpha)))%20*%20(1%20-%20%5Cmod((%5Ctheta_%7Bp_o%7D%2C360-%5Ctheta_%7Bp_s%7D%2B180%2C%20360))%2F180))

These functions denote that, given a person facing a stationary direction, how well a single person can engage with anyone. However, people usually turn their heads or bodies, and incur a discomfort factor. Suppose a person rotates \sigma degrees. Assume that it is not too difficult to turn. A beta value of .8 denotes a 20% loss when sitting perpindicular to your seat. The discomfort factor scales against the previous function, to find the following function:

\g(p_s,p_o,\sigma) = \f(p_s,p_o) * (90/(1-\beta)-abs(\sigma))/(90/(1-\beta))

