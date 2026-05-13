from vpython import *
#Web VPython 3.2

win = 500
Natoms = 500

L = 1
gray = color.gray(0.7)
mass = 4E-3/6E23
Ratom = 0.03
k = 1.4E-23
T = 300
dt = 1E-5

# Com que l'energia tèrmica és molt més gran que la potencial gravitatòria a nivell microscòpic, fem que mgL ~ kT.
g_eff = (k * T) / (mass * L)

animation = canvas(width=win, height=win, align='left')
animation.range = L
animation.title = 'Gas d\'esferes dures amb Termostat d\'Andersen i Gravetat'

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
pavg = sqrt(2*mass*1.5*k*T)

# Termostat d'Andersen (Q2)
nu = 500
prob_bany = nu * dt
sigma_p = sqrt(mass * k * T)

# Inicialitzem posicions i moments
for i in range(Natoms):
    x = L*random()-L/2
    y = L*random()-L/2
    z = L*random()-L/2
    if i == 0:
        Atoms.append(sphere(pos=vector(x,y,z), radius=Ratom, color=color.cyan, make_trail=True, retain=100, trail_radius=0.3*Ratom))
    else:
        Atoms.append(sphere(pos=vector(x,y,z), radius=Ratom, color=gray))
    apos.append(vec(x,y,z))

    # Repartiment inicial aleatori
    theta = pi*random()
    phi = 2*pi*random()
    px = pavg*sin(theta)*cos(phi)
    py = pavg*sin(theta)*sin(phi)
    pz = pavg*cos(theta)
    p.append(vector(px,py,pz))


# Gràfic de Vz
deltavz = 100
def barvz(vz):

    index = int((vz + 3000)/deltavz)
    if index < 0: index = 0
    if index >= int(6000/deltavz): index = int(6000/deltavz)-1
    return index

gvz = graph(width=win, height=0.4*win, xmax=3000, xmin=-3000, align='left', xtitle='Vz, m/s', ytitle='Number of atoms')
theory_vz = gcurve(color=color.blue, width=2)
dvz = 10
# Curva teòrica: Gaussiana 1D
for vz in range(-3000, 3001+dvz, dvz):
    theory_vz.plot(vz, (deltavz/dvz)*Natoms*sqrt(mass/(2*pi*k*T))*exp(-0.5*mass*(vz**2)/(k*T))*dvz)

accumvz = [[-3000 + deltavz*(i+.5), 0] for i in range(int(6000/deltavz))]
vzdist = gvbars(color=vector(0.88,0.5,0.76), delta=deltavz)

# Gràfic de les posicions Z
deltaz = 0.05
def barz(z):

    index = int((z + L/2)/deltaz)
    if index < 0: index = 0
    if index >= int(L/deltaz): index = int(L/deltaz)-1
    return index

gz = graph(width=win, height=0.4*win, xmax=L/2, xmin=-L/2, align='left', xtitle='Z position, m', ytitle='Number of atoms')
theory_z = gcurve(color=color.blue, width=2)
dz = 0.01
# Curva teòrica: Distribució baromètrica amb factor de normalització
z0_factor = Natoms * (mass * g_eff / (k * T)) / (1 - exp(-mass * g_eff * L / (k * T)))
for z in arange(-L/2, L/2 + dz, dz):
    theory_z.plot(z, deltaz * z0_factor * exp(-mass * g_eff * (z + L/2) / (k * T)))

accumz = [[-L/2 + deltaz*(i+0.5), 0] for i in range(int(L/deltaz))]
zdist = gvbars(color=color.orange, delta=deltaz)

def checkCollisions():
    hitlist = []
    r2 = 2*Ratom
    r2 *= r2
    for i in range(Natoms):
        ai = apos[i]
        for j in range(i) :
            aj = apos[j]
            dr = ai - aj
            if mag2(dr) < r2: hitlist.append([i,j])
    return hitlist

nhisto_count = 0

while True:
    rate(300)

    # Aplicació del Termostat d'Andersen
    for i in range(Natoms):
        if random() < prob_bany:

            u1, u2, u3, u4 = 1.0 - random(), random(), 1.0 - random(), random()
            z0 = sqrt(-2.0 * log(u1)) * cos(2 * pi * u2)
            z1 = sqrt(-2.0 * log(u1)) * sin(2 * pi * u2)
            z2 = sqrt(-2.0 * log(u3)) * cos(2 * pi * u4)
            p[i].x, p[i].y, p[i].z = sigma_p * z0, sigma_p * z1, sigma_p * z2

    # Actualització d'Histogrames
    histovz = [0.0] * int(6000/deltavz)
    histoz = [0.0] * int(L/deltaz)

    for i in range(Natoms):
        histovz[barvz(p[i].z / mass)] += 1
        histoz[barz(apos[i].z)] += 1

    for i in range(len(accumvz)):
        accumvz[i][1] = (nhisto_count*accumvz[i][1] + histovz[i])/(nhisto_count+1)
    for i in range(len(accumz)):
        accumz[i][1] = (nhisto_count*accumz[i][1] + histoz[i])/(nhisto_count+1)

    if nhisto_count % 10 == 0:
        vzdist.data = accumvz
        zdist.data = accumz
    nhisto_count += 1

    # Actualització de posicions i moments (Efecte de la gravetat)
    for i in range(Natoms):
        # Modificació Q3: Força gravitatòria constant actuant en sentit negatiu de l'eix Z
        p[i].z = p[i].z - (mass * g_eff) * dt

        Atoms[i].pos = apos[i] = apos[i] + (p[i]/mass)*dt

    hitlist = checkCollisions()

    # Resolució de col·lisions esfèriques
    for ij in hitlist:
        i, j = ij[0], ij[1]
        ptot = p[i]+p[j]
        posi, posj = apos[i], apos[j]
        vi, vj = p[i]/mass, p[j]/mass
        vrel = vj-vi
        a = vrel.mag2
        if a == 0: continue
        rrel = posi-posj
        if rrel.mag > Ratom: continue

        dx = dot(rrel, vrel.hat)
        dy = cross(rrel, vrel.hat).mag
        alpha = asin(dy/(2*Ratom))
        d = (2*Ratom)*cos(alpha)-dx
        deltat = d/vrel.mag

        posi = posi-vi*deltat
        posj = posj-vj*deltat
        mtot = 2*mass
        pcmi = p[i]-ptot*mass/mtot
        pcmj = p[j]-ptot*mass/mtot
        rrel = norm(rrel)
        pcmi = pcmi-2*pcmi.dot(rrel)*rrel
        pcmj = pcmj-2*pcmj.dot(rrel)*rrel
        p[i] = pcmi+ptot*mass/mtot
        p[j] = pcmj+ptot*mass/mtot
        apos[i] = posi+(p[i]/mass)*deltat
        apos[j] = posj+(p[j]/mass)*deltat

    # Rebots a les parets
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