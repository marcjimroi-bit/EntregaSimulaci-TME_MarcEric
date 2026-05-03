# --- TME: TREBALL DE SIMULACIÓ ---
# Secció 3: Creació d’una simulació pròpia
    # Codi i comentaris per: Marc Jiménez Roig

import numpy as np
import matplotlib.pyplot as plt
import math

# Paràmetres inicials
N = 1000
T_0 =300                # Temperatura inicial de prova (K)
k_B = 1.380649e-23      # Constant de Boltzmann (J K^-1)
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
epsilon = 1                             # Per simplicitat, \epsilon = 1
k_B = 1                                 # Per simplicitat. k_B = 1 implica \beta = 1/T, i [T] = energia
# Conjunt de valors de temperatura (k_B*T) estudiats. 
temps = np.concatenate([
    np.linspace(0.05, 5, 50),   # Molta densitat de punts a temperatures baixes (prop de t_c)
    np.linspace(5, 500, 50)     # Menys densitat de punts a temperatures molt altes
])
# Emmagatzemem els resultats obtinguts per les ocupacions mitjanes a cada nivell per cada temperatura
ocupacions = []

# A) ESTIMACIÓ DE L'ASSOLIMENT DE L'EQUILIBRI
# Busquem quants passos de la simulació són adequats per assolir un estat d'equilibri en un cas concret a T=T_test i extrapolem a la resta
t_test = 1.0
beta = 1 / (k_B * t_test)
estats = np.random.randint(0, 3, size=N)
occupacions_test = []

for j in range(50000):
    estats = pas_metropolis(estats, energies, beta)
    occupacions_test.append(np.sum(estats == 0) / N)

plt.plot(occupacions_test, color = 'darkred')
plt.ylim(0,1)
plt.tick_params(direction='in')
plt.grid(True)
plt.xlabel("Nombre de passos")
plt.ylabel(r'Ocupació del nivell $E_1=0$')
plt.show()

# Estimació de la temperatura crítica del problema 35 T_c
t_c = 10*epsilon/(k_B*math.log(N))
print(t_c)

# B) SIMULACIONS DEL SISTEMA PER CADA VALOR DE TEMPERATURA
for t in temps:
    beta = 1 / (t)

    # Establim l'estat inicial
    estats = np.random.randint(0, 3, size=N)

    # Simulem l'evolució del sistema mitjançant la funció definida segons la regla de Metropolis fins assolir l'equilibri
    n_pas = 10000
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

# Representació gràfica dels nivells d'ocupació per cada T
resultats_ocup = np.array(ocupacions)

plt.plot(temps, resultats_ocup[:, 0], label=r'$E_1=0$', color = 'darkred')
plt.plot(temps, resultats_ocup[:, 1], label=r'$E_2=\epsilon$', color = 'darkgreen')
plt.plot(temps, resultats_ocup[:, 2], label=r'$E_3=10\epsilon$', color = 'darkblue')
plt.axvline(x=t_c, linestyle=':', color='black', alpha = 1, label=r'$t_{\mathrm{c}}=1$')
plt.axhline(y=1/3, linestyle='--', color='black', alpha = 0.25)
plt.tick_params(direction='in')
plt.xscale('log')           # Per diferenciar t_c
plt.grid(True)
plt.xlabel(r'$t\equiv\frac{Tk_B}{\epsilon}$')
plt.ylabel("Ocupació mitjana")
plt.legend()
plt.show()


# ====================================================================================
# (3) ESTUDI DE LES FLUCTUACIONS ENERGÈTIQUES EN FUNCIÓ DE N
# Fixem la temperatura d'estudi t_a
t_a = 5.0

energies = np.array([0, 1, 10])

# Definim un conjunt de valors de N
Ns = [50, 100, 200, 500, 1000]

mitj_E = []
var_E = []

# Simulem el sistema per cada valor de N
for N in Ns:

    # Establim l'estat incial
    estats = np.random.randint(0, 3, size=N)

    # Simulem l'evolució del sistema mitjançant la funció definida segons la regla de Metropolis fins assolir l'equilibri
    n_pas = 10000
    for _ in range(n_pas):
        estats = pas_metropolis(estats, energies, beta)

    # Mesurem les ocupacions dels nivells
    mesures = 10000
    E_vals = []
    for _ in range(mesures):
        estats = pas_metropolis(estats, energies, beta)

        # Definim l'energia total a partir de les contribucions de cada nivell
        E_total = np.sum(energies[estats])
        E_vals.append(E_total)

    E_vals = np.array(E_vals)

    # Calculem el valor mitjà i variància de l'energia
    mitj_E.append(np.mean(E_vals))
    var_E.append(np.var(E_vals))  # variance = fluctuations

# B) Representació gràfica dels resultats
# i) Energia mitjana en funció de N
plt.plot(Ns, mitj_E, 'o-')
plt.tick_params(direction='in')
plt.xlabel("N")
plt.ylabel(r'$\langle E \rangle$')
plt.grid(True)
plt.show()

# ii) Variància / fluctuació de l'energia en funció de N
plt.plot(Ns, var_E, 'o-')
plt.tick_params(direction='in')
plt.xlabel("N")
plt.ylabel(r'$\sigma_E^2$')
plt.grid(True)
plt.show()

# iii) Fluctuació RELATIVA de l'energia en funció de N
fluct_rel = np.sqrt(var_E) / np.array(mitj_E)

plt.plot(Ns, fluct_rel, 'o-')
plt.tick_params(direction='in')
plt.xlabel("N")
plt.ylabel(r'$\sigma_E / \langle E \rangle$')
plt.grid(True)
plt.show()


# ------------------------------------------------------------------------------------
# END: Missatge final simulació
print('Run simulació complet.')