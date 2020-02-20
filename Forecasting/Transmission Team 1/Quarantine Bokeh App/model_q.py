"""
Quarantine ODE model wrapped in a function for use with the companion bokeh app

Model by L Liu, implemented initially by S Zhang, wrapped by B Chan

S Zhang | L Liu| B Chan | Feb 18th 2020
"""
import numpy as np
import scipy as sp
from scipy.integrate import odeint 
import matplotlib.pyplot as plt

def run_model(g_params, L_data, bats_param=20):

    def sigma(t):
        return 1/(1 + np.exp(t))

    travel_cutoff = 100
    bats_cutoff = bats_param
    z_func = lambda t: 4*sigma(2*(t-bats_cutoff))
    L_cutoff_func = lambda t: sigma(2*(t-travel_cutoff))

    def L(t):
        L = L_data.copy()
        L[0, :] = L[0, :]*L_cutoff_func(t)
        L[:, 0] = L[:, 0]*L_cutoff_func(t)
        return L

    def model(z_flat, t):
        z = np.reshape(z_flat, newshape = (6, M))
        s, eQ, eN, iQ, iN, r = [z[0, :], z[1, :], z[2, :], z[3, :], z[4, :], z[5, :]]
        n = np.sum(z, axis = 0)
        R0 = g_params['R0'] # Reproduction number R0 (same for all populations)
        De = g_params['De'] # Duration of exposure period
        Di = g_params['Di'] # Duration of infection
        alpha = g_params['alpha'] # indicator for Wuhan
        psi = g_params['psi'] # Fear level, 0 (none) < psi < 1 (max)
        phi = g_params['phi'] # Prob[infected individual able to travel]
        h = g_params['h'] # Infection rate in hospital, 0 < h < 1
        gamma = g_params['gamma'] # Prob[exposed individual is quarantined]
        Gamma = g_params['Gamma'] # 
        beta = g_params['beta'] # Prob[exposed individual is quarantined upon entry]
        tau = g_params['tau'] # Prob[infected individual is quarantined upon entry]
        
        ds = -s/n*(1-psi)*(R0/Di*iN + alpha*z_func(t) + h*R0/Di*iQ) + (np.matmul(np.transpose(L(t)), s/n) - s/n*np.matmul(L(t), np.ones(M)))
        deQ = gamma*s/n*(1-psi)*(R0/Di*iN + alpha*z_func(t) + h*R0/Di*iQ) - eQ/De + beta*(np.matmul(np.transpose(L(t)), eN/n))
        deN = (1-gamma)*s/n*(1-psi)*(R0/Di*iN + alpha*z_func(t) + h*R0/Di*iQ) - eN/De + (1-beta)*(np.matmul(np.transpose(L(t)), eN/n) - eN/n*np.matmul(L(t), np.ones(M)))
        diQ = (1-Gamma)*eN/De - iQ/Di + (1-tau)*(np.matmul(np.transpose(L(t)), iN/n) - phi*iN/n*np.matmul(L(t), np.ones(M)))                                                                                  
        diN = eQ/De + Gamma*eN/De - iN/Di + tau*(np.matmul(np.transpose(L(t)), iN/n)) 
        dr = iQ/Di + iN/Di + (np.matmul(np.transpose(L(t)), r/n) - r/n*np.matmul(L(t), np.ones(M)))
        dz = np.array([ds, deQ, deN, diQ, diN, dr])
        return np.reshape(dz, newshape = (1, 6*M))[0]


    M = 5
    c_params = [{''} for i in range(0, M)] # country-specific parameters
    #g_params = {'R0': 3, 'De': 6.5, 'Di': 7, 'alpha': np.zeros(M)} # global model parameters

    s0 = np.array([11.08e6, # Wuhan
                1.386e9, # Rest of China
                3.08e9,  # Rest of Asia 
                741e6,   # Europe
                579e6,   # North America
                ])
    eQ0 = np.zeros(M)
    eN0 = np.zeros(M)
    iQ0 = np.zeros(M)
    iN0 = np.zeros(M)
    r0 = np.zeros(M)
    z0 = np.array([s0, eQ0, eN0, iQ0, iN0, r0]) 

    n = 200
    t = np.linspace(0, 200, n)
    # solve ODE

    S = np.zeros((n, M))
    EQ = np.zeros((n, M))
    EN = np.zeros((n, M))
    IQ = np.zeros((n, M))
    IN = np.zeros((n, M))
    R = np.zeros((n, M))

    S[0] = z0[0, :]
    EQ[0] = z0[1, :]
    EN[0] = z0[2, :]
    IQ[0] = z0[3, :]
    IN[0] = z0[4, :]
    R[0] = z0[5, :]
        
    z0 = np.reshape(np.array([s0, eQ0, eN0, iQ0, iN0, r0]), newshape = (1, 6*M))[0] 

    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step 
        g_params['psi'] = np.array([0.8*i/n, ]*M)
        z = odeint(model,z0,tspan)[1]
        z = np.reshape(z, newshape = (6, M))
        
        S[i] = z[0, :]
        EQ[i] = z[1, :] 
        EN[i] = z[2, :]
        IQ[i] = z[3, :] 
        IN[i] = z[4, :]
        R[i] = z[5, :]

        z0 = np.reshape(z, newshape = (1, 6*M))[0]

    E = EQ + EN
    I = IQ + IN

    return t, I, E, R