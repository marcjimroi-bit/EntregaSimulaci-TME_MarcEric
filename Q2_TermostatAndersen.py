from vpython import *
#Web VPython 3.2

# Hard-sphere gas.

# Bruce Sherwood

win = 500

Natoms = 500  # change this to have more or fewer atoms
    # Durant la duració completa d'aquesta part, fixem Natoms = 500 (enunciat)
    # Sembla donar problemes de computació en la simulació (molt lent)

# Typical values
L = 1 # container is a cube L on a side
gray = color.gray(0.7) # color of edges of container
mass = 4E-3/6E23 # helium mass
Ratom = 0.03 # wildly exaggerated size of helium atom
    # Original Ratom = 0.03
k = 1.4E-23 # Boltzmann constant
T = 300 # around room temperature
dt = 1E-5

animation = canvas( width=win, height=win, align='left')
animation.range = L
animation.title = 'A "hard-sphere" gas'
s = """  Theoretical and averaged speed distributions (meters/sec).
  Initially all atoms have the same speed, but collisions
  change the speeds of the colliding atoms. One of the atoms is
  marked and leaves a trail so you can follow its path.
  
"""
animation.caption = s

d = L/2+Ratom
r = 0.005
boxbottom = curve(color=gray, radius=r)
boxbottom.append([vector(-d,-d,-d), vector(-d,-d,d), vector(d,-d,d), vector(d,-d,-d), vector(-d,-d,-d)])
boxtop = curve(color=gray, radius=r)
boxtop.append([vector(-d,d,-d), vector(-d,d,d), vector(d,d,d), vector(d,d,-d), vector(-d,d,-d)])
vert1 = curve(color=gray, radius=r)
vert2 = curve(color=gray, radius=r)
vert3 = curve(color=gray, radius=r)
vert4 = curve(color=gray, radius=r)
vert1.append([vector(-d,-d,-d), vector(-d,d,-d)])
vert2.append([vector(-d,-d,d), vector(-d,d,d)])
vert3.append([vector(d,-d,d), vector(d,d,d)])
vert4.append([vector(d,-d,-d), vector(d,d,-d)])

Atoms = []
p = []
apos = []
pavg = sqrt(2*mass*1.5*k*T) # average kinetic energy p**2/(2mass) = (3/2)kT

# Modificació Termostat Andersen
# --- Paràmetres del Termostat d'Andersen ---
nu = 500  # Freqüència de col·lisió amb el bany tèrmic (ajustable)
prob_bany = nu * dt  # Probabilitat de xocar en un interval dt
sigma_p = sqrt(mass * k * T)  # Desviació estàndard del moment: sqrt(m*k*T)

for i in range(Natoms):
    x = L*random()-L/2
    y = L*random()-L/2
    z = L*random()-L/2
    if i == 0:
        Atoms.append(sphere(pos=vector(x,y,z), radius=Ratom, color=color.cyan, make_trail=True, retain=100, trail_radius=0.3*Ratom))
    else: Atoms.append(sphere(pos=vector(x,y,z), radius=Ratom, color=gray))
    apos.append(vec(x,y,z))
    theta = pi*random()
    phi = 2*pi*random()
    px = pavg*sin(theta)*cos(phi)
    py = pavg*sin(theta)*sin(phi)
    pz = pavg*cos(theta)
    p.append(vector(px,py,pz))

deltav = 100 # binning for v histogram

def barx(v):
    return int(v/deltav) # index into bars array

nhisto = int(4500/deltav)
histo = []
for i in range(nhisto): histo.append(0.0)
histo[barx(pavg/mass)] = Natoms

gg = graph(width=win, height=0.4*win, xmax=3000, align='left',
    xtitle='speed, m/s', ytitle='Number of atoms', ymax=Natoms*deltav/1000)

theory = gcurve(color=color.blue, width=2)
dv = 10
for v in range(0,3001+dv,dv): # theoretical prediction
    theory.plot(v, (deltav/dv)*Natoms*4*pi*((mass/(2*pi*k*T))**1.5) *exp(-0.5*mass*(v**2)/(k*T))*(v**2)*dv)

accum = []
for i in range(int(3000/deltav)): accum.append([deltav*(i+.5),0])
vdist = gvbars(color=color.red, delta=deltav)

# --- ENERGIA ---
dE = 1e-21
Emax = 5e-20
nEbins = int(Emax/dE)
Ehisto = []
ymax_E = Natoms * (dE) * (2/sqrt(pi)) * (1/(k*T)**1.5) * sqrt(0.5 * k * T) * exp(-0.5)
Emax = 7 * k * T # per representar el 99% de les energies
for i in range(nEbins): Ehisto.append(0.0)

def barE(E):
    return int(E/dE)

gE = graph(width=win, height=0.4*win, align='right',
    xtitle='energy, J', ytitle='Number of atoms', xmax=Emax, xmin=0, ymin=0, ymax=ymax_E*1.2)

Edist = gvbars(color=color.green, delta=dE)

# --- CORBA TEÒRICA ENERGIA ---
theoryE = gcurve(color=color.blue, width=2)
dEt = dE/5  # més resolució que el bin
for E in arange(dEt, Emax, dEt):
    val = Natoms * (2/sqrt(pi)) * (1/(k*T)**1.5) * sqrt(E) * exp(-E/(k*T)) * dE
    theoryE.plot(E, val)

Eaccum = []
for i in range(nEbins): Eaccum.append([dE*(i+.5),0])

def interchange(v1, v2):  # remove from v1 bar, add to v2 bar
    barx1 = barx(v1)
    barx2 = barx(v2)
    if barx1 == barx2:  return
    if barx1 >= len(histo) or barx2 >= len(histo): return
    histo[barx1] -= 1
    histo[barx2] += 1

# --- ENERGIA ---
def interchange_E(E1, E2):
    b1 = barE(E1)
    b2 = barE(E2)
    if b1 == b2: return
    if b1 >= len(Ehisto) or b2 >= len(Ehisto): return
    Ehisto[b1] -= 1
    Ehisto[b2] += 1

def checkCollisions():
    hitlist = []
    r2 = 2*Ratom
    r2 *= r2
    for i in range(Natoms):
        ai = apos[i]
        for j in range(i):
            aj = apos[j]
            dr = ai - aj
            if mag2(dr) < r2: hitlist.append([i,j])
    return hitlist

nhisto = 0 # number of histogram snapshots to average

# --- ENERGIA (inicialització) ---
for i in range(Natoms):
    E = (p[i].mag**2)/(2*mass)
    if barE(E) < len(Ehisto):
        Ehisto[barE(E)] += 1

while True:

    for i in range(Natoms):
        if random() < prob_bany:
            v_antic = p[i].mag / mass
            E_antic = (p[i].mag**2)/(2*mass)  # --- ENERGIA ---
            # Generació de components del moment amb distribució gaussiana (Box-Muller)
            u1 = 1.0 - random() # Evitem el log(0)
            u2 = random()
            u3 = 1.0 - random()
            u4 = random()

            z0 = sqrt(-2.0 * log(u1)) * cos(2 * pi * u2)
            z1 = sqrt(-2.0 * log(u1)) * sin(2 * pi * u2)
            z2 = sqrt(-2.0 * log(u3)) * cos(2 * pi * u4)
            # Reassignem el moment de la partícula interaccionada
            p[i].x = sigma_p * z0
            p[i].y = sigma_p * z1
            p[i].z = sigma_p * z2
            # Actualitzem l'histograma de velocitats
            v_nou = p[i].mag / mass
            interchange(v_antic, v_nou)

            E_nou = (p[i].mag**2)/(2*mass)  # --- ENERGIA ---
            interchange_E(E_antic, E_nou)

    rate(300)
    # Accumulate and average histogram snapshots
    for i in range(len(accum)):
        accum[i][1] = (nhisto*accum[i][1] + histo[i])/(nhisto+1)

    if nhisto % 10 == 0:
        vdist.data = accum

    # --- ENERGIA ---
    for i in range(len(Eaccum)):
        Eaccum[i][1] = (nhisto*Eaccum[i][1] + Ehisto[i])/(nhisto+1)
    if nhisto % 10 == 0:
        Edist.data = Eaccum

    nhisto += 1
    # Update all positions
    for i in range(Natoms): Atoms[i].pos = apos[i] = apos[i] + (p[i]/mass)*dt
    
    # Check for collisions
    hitlist = checkCollisions()
    for i in range(Natoms):
        Atoms[i].pos = apos[i] = apos[i] + (p[i]/mass)*dt

    hitlist = checkCollisions()
    # If any collisions took place, update momenta of the two atoms
    for ij in hitlist:
        i = ij[0]
        j = ij[1]

        Ei = (p[i].mag**2)/(2*mass)  # --- ENERGIA ---
        Ej = (p[j].mag**2)/(2*mass)

        ptot = p[i]+p[j]
        posi = apos[i]
        posj = apos[j]
        vi = p[i]/mass
        vj = p[j]/mass
        vrel = vj-vi
        a = vrel.mag2
        if a == 0: continue  # exactly same velocities

        rrel = posi-posj
        if rrel.mag > Ratom: continue # one atom went all the way through another

    # theta is the angle between vrel and rrel:
        dx = dot(rrel, vrel.hat)       # rrel.mag*cos(theta)
        dy = cross(rrel, vrel.hat).mag # rrel.mag*sin(theta)
        # alpha is the angle of the triangle composed of rrel, path of atom j, and a line
        #   from the center of atom i to the center of atom j where atome j hits atom i:
        alpha = asin(dy/(2*Ratom))
        d = (2*Ratom)*cos(alpha)-dx # distance traveled into the atom from first contact
        deltat = d/vrel.mag         # time spent moving from first contact to position inside atom
        
        posi = posi-vi*deltat # back up to contact configuration
        posj = posj-vj*deltat
        mtot = 2*mass

        pcmi = p[i]-ptot*mass/mtot  # transform momenta to cm frame
        pcmj = p[j]-ptot*mass/mtot

        rrel = norm(rrel)
        pcmi = pcmi-2*pcmi.dot(rrel)*rrel  # bounce in cm frame
        pcmj = pcmj-2*pcmj.dot(rrel)*rrel

        p[i] = pcmi+ptot*mass/mtot  # transform momenta back to lab frame
        p[j] = pcmj+ptot*mass/mtot

        apos[i] = posi+(p[i]/mass)*deltat  # move forward deltat in time
        apos[j] = posj+(p[j]/mass)*deltat

        interchange(vi.mag, p[i].mag/mass)
        interchange(vj.mag, p[j].mag/mass)

        Ei_new = (p[i].mag**2)/(2*mass)  # --- ENERGIA ---
        Ej_new = (p[j].mag**2)/(2*mass)

        interchange_E(Ei, Ei_new)
        interchange_E(Ej, Ej_new)

    for i in range(Natoms):
        loc = apos[i]
        if abs(loc.x) > L/2:
            if loc.x < 0: p[i].x = abs(p[i].x)
            else: p[i].x = -abs(p[i].x)

        if abs(loc.y) > L/2:
            if loc.y < 0: p[i].y = abs(p[i].y)
            else: p[i].y = -abs(p[i].y)

        if abs(loc.z) > L/2:
            if loc.z < 0: p[i].z = abs(p[i].z)
            else: p[i].z = -abs(p[i].z)