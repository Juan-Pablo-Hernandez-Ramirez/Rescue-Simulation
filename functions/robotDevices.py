from controller import Robot
robot = Robot()





timeStep = 16
# speed_max = 6.28
speed_max = 4.5
speed_med = 4.3
speed_ordynary = 4
speed_baj = 3.5
count = 1
step_c = 1
step_giro = 150
step_u = 140
ts = 120  # 55 #79
tg = 65  # 100
lg = 70  # 125
envio_m = False

d_fd = 0  # Distancia a la pared sensor frontal derecho
d_fi = 0  # Distancia a la pared sensor frontal izquierdo
d_dd = 0  # Distancia a la pared sensor derecho delantero
d_dc = 0  # Distancia a la pared sensor derecho central
d_id = 0  # Distancia a la pared sensor izquierdo delantero
d_ic = 0  # Distancia a la pared sensor izquierdo central

l_fd = 1  # Valor logico existe pared sensor frontal derecho
l_fi = 1  # Valor logico existe pared frontal derecho
l_dd = 1  # Valor logico existe pared sensor  derecho delantero
l_dc = 1  # Valor logico existe pared sensor  derecho central
l_id = 1  # Valor logico existe pared sensor izquierdo delantero
l_ic = 1  # Valor logico existe pared sensor izquierdo central

inercia = 'F'  # recuerda en que sentido se mueve el robot (F) al frente (I) izaquierda (D) derecha (U) en U
inercia_ant = 'F'
inaux = ""
cont_ant = 0
per_lect_gps = 0
x = 0
y = 0
z = 0
camG = ""
enc_victima = ""
tipo_victima = "N"
contGVic = 0
vi = [] # Vector de inercias
lectse=25

muros     = 180 # Distancia a los muros para tomar la pared
frente    = 100 # Distancia al frente para tomar la pared
lejos     = 250 # Distancia en la que los sensores no pueden sentrarse
mas_lejos = 800 # Distancia maxima en la que los sonsores detectan algo
media     = 60  # Distancia ideal de la pared izquierda

pantano   = 1   # Multiplicador por pantano

cada = 10
cuantos = 0
sigue = 0

# Definir los movimientos
paso = 0
count_der = 35
count_izq = 35
count_fte = 80
inicio = 1  # Pasos iniciales para que no se vaya al pozo

# Victimas visuales
v_visual = False
dif_paredes = 10
victimTimer = 0
contC = 0
contA = 0
contR = 0
contVic = 0







rueda_rdf = robot.getDevice("wheel2 motor")
rueda_rif = robot.getDevice("wheel1 motor")
rueda_rdf.setPosition(float('inf'))
rueda_rif.setPosition(float('inf'))

# sensores de distancia
sensor_fd = robot.getDevice("ps0")
sensor_fd.enable(timeStep)
sensor_fi = robot.getDevice("ps7")
sensor_fi.enable(timeStep)
sensor_dd = robot.getDevice("ps1")
sensor_dd.enable(timeStep)
sensor_dc = robot.getDevice("ps2")
sensor_dc.enable(timeStep)
sensor_id = robot.getDevice("ps6")
sensor_id.enable(timeStep)
sensor_ic = robot.getDevice("ps5")
sensor_ic.enable(timeStep)

# Camaras y sensor de color
c_color = robot.getDevice("colour_sensor")
c_color.enable(timeStep)
camera = robot.getDevice("camera_centre")
camera.enable(timeStep)
camerar = robot.getDevice("camera_right")
camerar.enable(timeStep)
cameral = robot.getDevice("camera_left")
cameral.enable(timeStep)

## Emisor y recividor
emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")

# Declara GPS
gps = robot.getDevice("gps")
# gps = robot.getGPS("gps")
gps.enable(timeStep)
lect_gps = gps.getValues()