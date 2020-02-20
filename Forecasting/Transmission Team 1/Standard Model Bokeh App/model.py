"""
Non-Quarantine ODE model wrapped in a function for use with the companion bokeh app

S Zhang | L Liu | R Cardim-Falco | S Iyaniwura | M Kellas-Dicks | D Cameron | B Chan | Feb 18th 2020
"""
import numpy as np
import scipy as sp
from scipy.integrate import odeint 
import matplotlib.pyplot as plt

def ode_model(R0_in=2, De_in=4, Di_in=8):
    def model(z_flat, t):
        z = np.reshape(z_flat, newshape = (4, M))
        s, e, i, r = [z[0, :], z[1, :], z[2, :], z[3, :]]
        n = np.sum(z, axis = 0)
        R0 = R0_in #g_params['R0']
        De = De_in #g_params['De']
        Di = Di_in #g_params['Di']

        ds = -s/n*(R0/Di*i) + (n/n0)*(np.matmul(np.transpose(L), s/n) - s/n*np.matmul(L, np.ones(M)))
        de = s/n*(R0/Di*i) - e/De + (n/n0)*(np.matmul(np.transpose(L), e/n) - e/n*np.matmul(L, np.ones(M)))
        di = e/De - i/Di + (n/n0)*(np.matmul(np.transpose(L), i/n) - i/n*np.matmul(L, np.ones(M)))
        dr = i/Di + (n/n0)*(np.matmul(np.transpose(L), r/n) - r/n*np.matmul(L, np.ones(M)))
        dz = np.array([ds, de, di, dr])
        return np.reshape(dz, newshape = (1, 4*M))[0]
    
    # consider M countries 
    M = 3
    n0 = 100
    c_params = [{''} for i in range(0, M)] # country-specific parameters
    #g_params = {'R0': 2, 'De': 4, 'Di': 8} # global model parameters
    L = np.zeros((M, M)) # matrix of travel rates; L(i, j) = rate of travel from country i --> country j

    s0 = np.array([100, ]*M)
    e0 = np.zeros(M)
    i0 = np.zeros(M)
    i0[0] = 1
    r0 = np.zeros(M)
    z0 = np.array([s0, e0, i0, r0]) # z = [s e i r]

    n = 2000
    t = np.linspace(0, 500, n)
    # solve ODE

    S = np.zeros((n, M))
    E = np.zeros((n, M))
    I = np.zeros((n, M))
    R = np.zeros((n, M))

    S[0] = z0[0, :]
    E[0] = z0[1, :]
    I[0] = z0[2, :]
    R[0] = z0[3, :]
        
    z0 = np.reshape(np.array([s0, e0, i0, r0]), newshape = (1, 4*M))[0] # z = [s e i r]

    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        z = odeint(model,z0,tspan)[1]
        z = np.reshape(z, newshape = (4, M))
        
        S[i] = z[0, :]
        E[i] = z[1, :]
        I[i] = z[2, :]
        R[i] = z[3, :]

        z0 = np.reshape(z, newshape = (1, 4*M))[0]

    return t, S, I, E