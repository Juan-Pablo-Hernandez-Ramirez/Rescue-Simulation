# ------------------------------------ #
# ----- Importacion de librerias ----- #
# ------------------------------------ #

from sys import path
from re  import X
from matplotlib.contour import ContourSet

import os.path



path.append("../classes")
from c_imagen  import imagen_ref
from c_victima import victima

path.append("../detection")
from victimDetection import *

path.append("../functions")
from directions   import *
from robotDevices import  *



useCV = False
try:
    from controller import Robot  # Conexión del controlador al objeto Robot
    import math, struct, time, cv2

    useCV = True
    import numpy as np

    camara_victima = True  # Comprobamos la funcionalidad de librerias como opencv y numpy
    viewHSV = True
except:
    print("Librerias no instaladas")



# Crear un objeto de la clase robot
listaGp  = []
indice   = 0
timeStep = 16


# Definición de variables

########################################


# ----------------------------------------- #
# ----- Busqueda de victimas visuales ----- #
# ----------------------------------------- #

def delay(ms):
    initTime = robot.getTime()  # Store starting time (in seconds)
    while robot.step(timeStep) != -1:
        if (robot.getTime() - initTime) * 1000.0 > ms:  # If time elapsed (converted into ms) is greater than value passed in
            break



def report():
    global envio_m, inercia, contC, enc_victima
    print("se envio el mensaje: ", envio_m)
    if envio_m == False:
        paro()
        print("enc_victima ", enc_victima)
        delay(1300)
        # print("Termina espera...")
        # victimType = bytes('H', "utf-8")
        victimType = bytes(enc_victima, "utf-8")
        posX = dat_victima.getPosx()
        posZ = dat_victima.getPosz()
        message = struct.pack("i i c", posX, posZ, victimType)
        print(message)
        emitter.send(message)
        robot.step(timeStep)
        envio_m = True
        contC = 0
        enc_victima = ""
        tipo_victima = ""
        dat_victima.setCamara("")
        dat_victima.setPosx(0)
        dat_victima.setPosz(0)
        dat_victima.setTipo("")
        dat_victima.setValor(0)
    else:
        envio_m = False
        contVic = 0




###############################################################################################

# Procedimiento de lectura de sensores de distancia
def lee_distancia():
    global d_fd
    global d_fi
    global d_dd
    global d_dc
    global d_id
    global d_ic
    global l_fd
    global l_fi
    global l_dd
    global l_dc
    global l_id
    global l_ic

    d_fd = int(sensor_fd.getValue() * 1000)
    d_fi = int(sensor_fi.getValue() * 1000)
    d_dd = int(sensor_dd.getValue() * 1000)
    d_dc = int(sensor_dc.getValue() * 1000)
    d_id = int(sensor_id.getValue() * 1000)
    d_ic = int(sensor_ic.getValue() * 1000)

    if (d_ic > 500 and d_id < frente):
        print("estoy pagado a la pared izquierda")
        d_ic = 0

    if (d_dc > 500 and d_dd < frente):
        print("estoy pagado a la pared derecha")
        d_dc = 0

    '''if (d_fd>600 and d_fi>600 and (d_dd<frente or d_id<frente)):
        print("estoy pagado a la pared frontal a la derecha")
        d_fd=0
        d_fi=0'''

    if (d_fd > 600 and d_dd < frente):
        print("estoy pagado a la pared frontal a la derecha")
        d_fd = 0

    if (d_fi > 600 and d_id < frente):
        print("estoy pagado a la pared frontal a la izquierda")
        d_fi = 0

    ## logicos al frente
    if (d_fd > frente):
        l_fd = 1  ## no hay pared al frente
    else:
        l_fd = 0  ## hay pared al frente

    if (d_fi > frente):
        l_fi = 1  ## no hay pared al frente
    else:
        l_fi = 0  ## hay pared al frente

    ## logicos a las paredes
    if (d_dd > muros):
        l_dd = 1  ## no hay pared a la derecha
    else:
        l_dd = 0  ## hay pared a la derecha

    if (d_dc > muros):
        l_dc = 1  ## no hay pared a la derecha
    else:
        l_dc = 0  ## hay pared a la derecha

    if (d_id > muros):
        l_id = 1  ## no hay pared a la izquierda
    else:
        l_id = 0  ## hay pared a la izquierda

    if (d_ic > muros):
        l_ic = 1  ## no hay pared a la izquierda
    else:
        l_ic = 0  ## hay pared a la izquierda

    # print('distancia fd ', d_fd,'  fi ', d_fi,' derecha delantero ',d_dd,' derecha central ',d_dc," izquierda delantero ",d_id," izquierda central ",d_ic)
    print('logica fd ', l_fd,'  fi ', l_fi,' derecha delantero ',l_dd,' derecha central ',l_dc," izquierda delantero ",l_id," izquierda central ",l_ic)


# Lectura del color del piso
def prueba_color():
    global ts
    global tg
    global lg
    global step_c
    global speed_ordynary
    global pantano
    color = c_color.getImage()
    print(color)
    speed_ordynary = 4
    pantano = 1
    if color in [b'\x8e\xde\xf4\xff', b'\x8c\xdc\xf3\xff', b'\x8d\xdd\xf4\xff', b'\x81\xd1\xed\xff',
                 b'\x81\xd2\xed\xff', b'\x81\xd1\xec\xff', b'\x80\xd0\xec\xff', b'\x7f\xd0\xec\xff',
                 b'\x82\xd3\xee\xff', b'\x83\xd3\xee\xff', b'\x83\xd4\xee\xff', b'\x89\xd9\xf2\xff',
                 b'\x7f\xcf\xeb\xff', b'\xfe\xfe\xfe\xff', b'\x84\xd4\xef\xff', b'~\xce\xea\xff',
                 b'\x7f\xd0\xeb\xff', b'\x88\xd8\xf1\xff', b'}\xcd\xea\xff', b'\x80\xd0\xec\xff',
                 b'\x82\xd2\xed\xff']:
        # print("------------------------------------------------------PANTANO")
        pantano = 2
        speed_ordynary = 2
    elif color in [b';;;\xff', b';;@\xff', b'ooo\xff', b'---\xff', b'<<<\xff']:
        # print("------------------------------------------------------TRAMPA")
        step_c = 55
        sal_trampa()


def lee_gps():
    global lect_gps
    global x
    global y
    global z
    global inercia
    lect_gps = gps.getValues()
    print(lect_gps)
    xa = x
    za = z
    x = int(lect_gps[0] * 1000)
    y = int(lect_gps[1] * 1000)
    z = int(lect_gps[2] * 1000)
    # print("leyendo gps x-",x,"y-",y,"z-",z)
    if (xa == x and za == z and inercia == "F"):
        print("Estancado")
        inercia = "U"


def guardagps():
    lectura= gps.getValues()
    print(lectura)
    x = int(lectura[0] * 1000)
    z = int(lectura[2] * 1000)



## Programa principal (main)
while robot.step(timeStep) != -1:
    # print("---------------------------------------------------------------------")
    # print("inicio: ",inicio," paso: ", paso," count ",count," pantano ", pantano," per_gps", per_lect_gps)
    if (per_lect_gps == 25):
        lee_gps()
        per_lect_gps = 0
    else:
        per_lect_gps = per_lect_gps + 1

    prueba_color()
    lee_distancia()
    direccion()

    # paro()

    print("EntVictima = ", enc_victima)
    if (enc_victima != ""):
        inclinacionesVictim(cam_enc)
        val_act = checkVic()
        if contVic >= contGVic:
            report()
            inercia = "F"
            print("inercia al salir de reporte ", inercia)
            contVic  = 0
            contGVic = 0
            camG = ""
        else:
            print("enc_victima=", enc_victima, " cont ", contVic)
            contVic = contVic + (1 / pantano)
    else:
        print("Leo camaras...")
        leer_camaras()
    #time.sleep(0.5)