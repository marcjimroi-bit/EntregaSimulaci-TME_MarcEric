import numpy as np
import matplotlib.pyplot as plt
import math

# Paràmetres inicials
N = 1000
T_0 =300        # Temperatura inicial de prova (K)
k_B = 1.380649e-23  # Constant de Boltzmann (J K^-1)
beta = 1/(k_B * T_0)
e1 = 0
e2 = 1
e3 = 10
energies = np.array([e1,e2,e3])      # Nivells d'energia considerats (\epsilon = 1)

# Definim un array per l'estat de N partícules, que inicialment estan repartides amb igual probabilitat entre cada nivell (probabilitat = 1/3)
estats = np.random.choice([e1,e2,e3],N)

# 1) REGLA DE METROPOLIS
    # El sistema evolucionarà segons com les partícules augmentin o disminueixin la seva energia (\Delta E)
        # Tendència generalitzada a reduir la seva energia (\Delta E < 0)
        # Bany tèrmic augmenta energia (\Delta E > 0); salts grans molt menys probables que petits.

def pas_metropolis(estats, nivells, beta):
    
    # a) Escollim una partícula aleatòriament
    i = np.random.randint(0,N)
    nivell_abans = estats[i]

    # b) Proposem un canvi a un nou nivell energètic (índex del nivell)
    nivell_després = np.random.randint(0,3)
        # Ens assegurem que sempre hi hagi un canvi de nivell
    while nivell_després == nivell_abans:
        nivell_després = np.random.randint(0, 3)
    
    # c) Diferència d'energies (\Delta E) i acceptació segons Metropolis
    dE = energies[nivell_després] - energies[nivell_abans]
        # Per \Delta E <= 0 acceptem el canvi sempre
        # Per \Delta E > 0 hi ha una probabilitat (entre 0 i 1) que s'accepti o no en funció de exp(-beta * dE)
    if dE <= 0 or np.random.rand() < np.exp(-beta * dE):
        estats[i] = nivell_després 

    return estats

