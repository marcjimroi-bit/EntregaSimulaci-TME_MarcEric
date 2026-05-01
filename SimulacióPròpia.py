import numpy as np
import matplotlib.pyplot as plt
import math

# Paràmetres inicials
N = 1000
T_0 =300        # Temperatura inicial de prova
e1 = 0
e2 = 1
e3 = 10
nivells = np.array([e1,e2,e3])      # Nivells d'energia considerats (\epsilon = 1)

# Definim un array per l'estat de N partícules, que inicialment estan repartides amb igual probabilitat entre cada nivell (probabilitat = 1/3)
estats = np.random.choice([e1,e2,e3],N)
