# ------------------------- Importacion de librerias ------------------------- #

from sys import path
from re  import X
from matplotlib.contour import ContourSet

import os.path

# ------------------------- Importacion de modulos ------------------------- #

path.append("../classes")
from c_imagen  import imagen_ref
from c_victima import victima

path.append("../detection")
from victimDetection import *
from sensorReading import *

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
indice   = 0
timeStep = 16


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
        posX = dat_victima.getPosX()
        posZ = dat_victima.getPosZ()
        message = struct.pack("i i c", posX, posZ, victimType)
        print(message)
        emitter.send(message)
        robot.step(timeStep)
        envio_m = True
        contC = 0
        enc_victima = ""
        tipo_victima = ""
        dat_victima.setCamara("")
        dat_victima.setPosX(0)
        dat_victima.setPosZ(0)
        dat_victima.setTipo("")
        dat_victima.setValor(0)
    else:
        envio_m = False
        contVic = 0




###############################################################################################

# Lectura del color del piso
def prueba_color():
    global ts, tg, lg, step_c, speed_ordynary, pantano
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
    global lect_gps, inercia, x, y, z
    lect_gps = gps.getValues()
    print(lect_gps)
    xa = x
    za = z
    x = int(lect_gps[0] * 1000)
    y = int(lect_gps[1] * 1000)
    z = int(lect_gps[2] * 1000)
    print("leyendo gps x-",x,"y-",y,"z-",z)
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