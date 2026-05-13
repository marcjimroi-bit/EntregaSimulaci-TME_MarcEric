from vpython import *

# 1. Configuració de la finestra (canvas)
# L'alineació a la esquerra sol ajudar a que el navegador ho gestioni millor
scene = canvas(width=800, height=600, align='left', title='Eina de Selecció de Colors per a VPython')

# 2. Mostra de colors estàndard per referència ràpida
standard_colors = [
    ('Vermell', color.red), ('Verd', color.green), ('Blau', color.blue),
    ('Cian', color.cyan), ('Magenta', color.magenta), ('Groc', color.yellow),
    ('Taronja', color.orange), ('Lila', color.purple), ('Gris', color.gray(0.5))
]

label(pos=vector(0, 3, 0), text="Colors predefinits de VPython:", height=15, box=False)

for i, c in enumerate(standard_colors):
    x_pos = -4 + i * 1
    box(pos=vector(x_pos, 2, 0), size=vector(0.8, 0.8, 0.1), color=c[1])
    label(pos=vector(x_pos, 1.3, 0), text=c[0], height=10, box=False)

# 3. Zona de proves dinàmica
label(pos=vector(0, 0, 0), text="Barreja el teu propi color (RGB):", height=15, box=False)
mostra = box(pos=vector(0, -1.5, 0), size=vector(4, 1.5, 0.2), color=vector(0.5, 0.5, 0.5))
codi_text = label(pos=vector(0, -3, 0), text="", height=20, color=color.yellow, border=4)

# Funció que s'executa quan mous els sliders
def actualitzar():
    r = sl_r.value
    g = sl_g.value
    b = sl_b.value
    
    # Actualitzem el color del cub central
    nou_color = vector(r, g, b)
    mostra.color = nou_color
    
    # Generem el text que hauràs de copiar al teu codi de la simulació
    # Round a 2 decimals per que el codi no sigui infinit
    codi_text.text = f"Codi: color=vector({round(r,2)}, {round(g,2)}, {round(b,2)})"

# 4. Creació dels Sliders al peu de la pàgina (caption)
scene.caption = "\n<b>Ajusta els canals de color:</b>\n\n"

sl_r = slider(min=0, max=1, value=0.5, bind=actualitzar, color=color.red)
scene.append_to_caption(" Vermell (R)\n\n")

sl_g = slider(min=0, max=1, value=0.5, bind=actualitzar, color=color.green)
scene.append_to_caption(" Verd (G)\n\n")

sl_b = slider(min=0, max=1, value=0.5, bind=actualitzar, color=color.blue)
scene.append_to_caption(" Blau (B)\n\n")

# Inicialitzem el text per primer cop
actualitzar()

# Bucle buit per mantenir la finestra oberta
while True:
    rate(30)