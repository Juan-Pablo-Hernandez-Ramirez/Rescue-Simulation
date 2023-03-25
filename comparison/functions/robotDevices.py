from controller import Robot

robot = Robot() # Creacion de un objeto robot de la clase robot

# ------------------------- Velocidades del robot ------------------------- #

timeStep = 16
speed_max = 4.5    # Velocidad maxima del robot
speed_med = 4.3    # Velocidad media
speed_ordynary = 4 # Velocidad ordinaria
speed_baj = 3.5    # Velocidad baja del robot


# ------------------------- Pasos del robot ------------------------- #

count = 1
step_c = 1
step_giro = 150
step_u = 140
ts = 120 # 55 #79
tg = 65  # 100
lg = 70  # 125
envio_m = False

# ------------------------- Distancias de los sensores ------------------------- #


# Se lee la distancia de los sensores hacia las paredes
d_frontalDerecha     = 0 # Distancia de los sensores hacia la pared
d_frontalIzquierda   = 0
d_delanteraDerecha   = 0
d_centralDerecha     = 0
d_delanteraIzquierda = 0
d_centralizquierda   = 0


# Valores logicos que se utilizan para convertir la distancia a un numero binario
l_frontalDerecho     = 1  # Valor logico existe pared sensor frontal derecho
l_frontalIzquierdo   = 1
l_delanteroDerecho   = 1
l_delanteroIzquierdo = 1
l_centralDerecho     = 1
l_centralIzquierdo   = 1

inercia = 'F'   # Guarda la direccion en la que se esta moviendo el robot
                # (F) Frente
                # (I) Izquierda
                # (D) Derecha
                # (U) Girando en U


inercia_ant = 'F' # Guarda la distancia previa en la que se movio el robot
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

ruedaIzquierda = robot.getDevice("wheel1 motor")
ruedaIzquierda.setPosition(float('inf'))

ruedaDerecha = robot.getDevice("wheel2 motor")
ruedaDerecha.setPosition(float('inf'))


# ------------------------- sensores de distancia ------------------------- #

# Senores frontales
sensorFrontalDerecho = robot.getDevice("ps0")
sensorFrontalDerecho.enable(timeStep)
sensorFrontalIzquierdo = robot.getDevice("ps7")
sensorFrontalIzquierdo.enable(timeStep)

# Senores delanteros
sensorDelanteroDerecho = robot.getDevice("ps1")
sensorDelanteroDerecho.enable(timeStep)
sensorDelanteroIzquierdo = robot.getDevice("ps6")
sensorDelanteroIzquierdo.enable(timeStep)

# Senores centrales
sensorCentralIzquierdo = robot.getDevice("ps5")
sensorCentralIzquierdo.enable(timeStep)
sensorCentralDerecho = robot.getDevice("ps2")
sensorCentralDerecho.enable(timeStep)

# Camaras y sensor de color
c_color = robot.getDevice("colour_sensor")
c_color.enable(timeStep)
camaraCentral = robot.getDevice("camera_centre")
camaraCentral.enable(timeStep)
camaraDerecha = robot.getDevice("camera_right")
camaraDerecha.enable(timeStep)
camaraIzquierda = robot.getDevice("camera_left")
camaraIzquierda.enable(timeStep)

## Emisor y recividor
emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")

# Declara GPS
gps = robot.getDevice("gps")
# gps = robot.getGPS("gps")
gps.enable(timeStep)
lect_gps = gps.getValues()