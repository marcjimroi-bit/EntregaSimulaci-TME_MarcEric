# --- TME: TREBALL DE SIMULACIÓ ---
# Secció 3: Creació d’una simulació pròpia
    # Codi i comentaris per: Marc Jiménez Roig

import numpy as np
import matplotlib.pyplot as plt
import math

# Paràmetres inicials
N = 1000
T_0 =300        # Temperatura inicial de prova (K)
k_B = 1         # Per simplicitat. Físicament, constant de Boltzmann = 1.380649e-23 J K^-1
beta = 1/(k_B * T_0)
energies = np.array([0,1,10])      # Nivells d'energia considerats (\epsilon = 1)

# ====================================================================================
# (1) TEST CAS INDIVIDUAL
# Definim un array per l'estat de N partícules a temperatura T_0, que inicialment estan repartides amb igual probabilitat entre cada nivell (probabilitat = 1/3)
estats = np.random.randint(0, 3, size=N)

# A) REGLA DE METROPOLIS
    # El sistema evolucionarà segons com les partícules augmentin o disminueixin la seva energia (\Delta E)
        # Tendència generalitzada a reduir la seva energia (\Delta E < 0)
        # Bany tèrmic augmenta energia (\Delta E > 0); salts grans molt menys probables que petits.
def pas_metropolis(estats, energies, beta):
    
    # i) Escollim una partícula aleatòriament
    i = np.random.randint(0,N)
    nivell_abans = estats[i]

    # ii) Proposem un canvi a un nou nivell energètic (índex del nivell)
    nivell_després = np.random.randint(0,3)
        # Ens assegurem que sempre hi hagi un canvi de nivell
    while nivell_després == nivell_abans:
        nivell_després = np.random.randint(0, 3)
    
    # iii) Diferència d'energies (\Delta E) i acceptació segons Metropolis
    dE = energies[nivell_després] - energies[nivell_abans]
        # Per \Delta E <= 0 acceptem el canvi sempre
        # Per \Delta E > 0 hi ha una probabilitat (entre 0 i 1) que s'accepti o no en funció de exp(-beta * dE)
    if dE <= 0 or np.random.rand() < np.exp(-beta * dE):
        estats[i] = nivell_després 

    return estats

# B) SIMULACIÓ DE L'EVOLUCIÓ DEL SISTEMA
# Apliquem la funció anterior i simulem els passos fins assolir un estat d'equilibri
n_pas = 1000
for j in range(n_pas):
    estats = pas_metropolis(estats, energies, beta)

# Ocupació mitjana en l'equilibri: Definim un nombre molt gran de mesures, les quals aplicarem a estats d'equilibri
num_niv = np.zeros(3)
mesures = 10000

# Un cop assolit l'equilibri (evolució anterior), seguim evolucionant el sistema (ara en equilibri) i mesurem la ocupació de cada nivell
for j in range(mesures):
    estats = pas_metropolis(estats, energies, beta)
    for nivell in range(3):
        num_niv[nivell] += np.sum(estats == nivell)
# Normalitzem les mesures respecte el total
avg_occupation = num_niv / (mesures * N)
print(avg_occupation)


# ====================================================================================
# (2) ESTUDI EN FUNCIÓ DE LA TEMPERATURA
# Definim un conjunt de valors equiespaiats de temperatura que cobreixin un rang prou gran per tal d'estudiar-ne la dependència.
energies = np.array([0,1,10])           # Respecte \epsilon
temps = np.linspace(0.1, 100, 100)       # k_B = 1 implica \beta = 1/T, i [T] = energia
# Emmagatzemem els resultats obtinguts per les ocupacions mitjanes a cada nivell per cada temperatura
ocupacions = []

# A) SIMULACIONS DEL SISTEMA PER CADA VALOR DE TEMPERATURA
for T in temps:
    beta = 1 / (k_B * T)

    # Establim l'estat inicial
    estats = np.random.randint(0, 3, size=N)

    # Simulem l'evolució del sistema mitjançant la funció definida segons la regla de Metropolis fins assolir l'equilibri
    n_pas = 1000
    for j in range(n_pas):
        estats = pas_metropolis(estats, energies, beta)

    # Mesurem les ocupacions dels nivells (un nombre gran de mesures permet mantenir-nos en condicions d'equilibri)
    num_niv = np.zeros(3)
    mesures = 10000
    # Mesures de les ocupacions de cada nivell per iteracions en condicions d'equilibri
    for j in range(mesures):
        estats = pas_metropolis(estats, energies, beta)
        for nivell in range(3):
            num_niv[nivell] += np.sum(estats == nivell)
    # Normalització
    avg_occ = num_niv / (mesures * N)
    ocupacions.append(avg_occ)

# B) REPRESENTACIÓ GRÀFICA DELS RESULTATS ANTERIORS
resultats_ocup = np.array(ocupacions)

for nivell in range(3):
    plt.plot(temps, resultats_ocup[:, nivell], label=f"Nivell {nivell}")

plt.xlabel(r'$T$ (K)')
plt.ylabel("Ocupació mitjana")
plt.legend()
plt.show()

# ------------------------------------------------------------------------------------
# END: Missatge final simulació
print('Run simulació complet.')