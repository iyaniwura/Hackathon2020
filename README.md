![alt-text](images/norwester_blue.png)
# EpiCoronaHack 2020 - Team Quarantine (transmission)

## Team Member:

* David Cameron (BC Cancer)
* Brandon Chan (BC Cancer)
* Rebeca Cardim Falcao (UBC)
* Sarafa Iyaniwura (UBC)
* Mechthild Kellas-Dicks 
* Liangchen Liu (UBC)
* Stephen Zhang (UBC)

## Team Aim:

* Build a ODE metapopulation model for different regions 
  * without  quarantine
  * with quarantine 
* Use numerical simulation (in Python) to determine the effect of different intervention strategies on local outbreak prevention and control; (Perhaps) BCCDC professionals can determine the most effective and economical  control measures based on this. 
* Develop visualization tools to aid in model parameter investigation, selection, and outcomes. 
* The tools can be used to investigate the sensitivity of the parameters of the model.

## Team Progress:

We already have the (primary) model, we coded it up, we nunmerically solved the systems of ODEs and ran simulations based on some made-up data (Team Flight we need you!), and we have the visualization!

## The mathematical Model

* S_i(t) susceptible population in the $i^{th}$ city
* E(t) susceptible population in the $i^{th}$ city
* I(t) susceptible population in the $i^{th}$ city


* Without quarantine

![alt-text](images/ODE_NoQuarantine.png)


* With quarantine

![alt-text](images/ODE_Quarantine.png)

