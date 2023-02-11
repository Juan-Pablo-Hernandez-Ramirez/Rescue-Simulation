# ------------------------------------ #
# ----- Importacion de librerias ----- #
# ------------------------------------ #

import os.path
from sys import path
path.append("../functions")
from robotDevices import  *
from directions  import *


path.append("../classes")
from c_imagen  import imagen_ref
from c_victima import victima


from re import X
from matplotlib.contour import ContourSet



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
listaGps           = []
central_refference = []
left_refference    = []
right_refference   = []


def encontrar_tipo(ind):
    if   (ind <= 5):
        tip = "H"
    elif (ind <= 11):
        tip = "S"
    elif (ind <= 17):
        tip = "U"
    elif (ind <= 23):
        tip = "C"
    elif (ind <= 29):
        tip = "P"
    elif (ind <= 35):
        tip = "F"
    elif (ind <= 41):
        tip = "O"
    return tip


def encontrar_color(ind):
    # ---------- H  H, S   S,  U   U,  C   C,  P   P,  F   F,  O,  O  #
    if   ind in [0, 1, 6,  7,  12, 13, 18, 19, 24, 25, 30, 31, 36, 37]:
        col_fdo = "B"

    elif ind in [2, 3, 8,  9,  14, 15, 20, 21, 26, 27, 32, 33, 38, 39]:
        col_fdo = "N"

    elif ind in [4, 5, 10, 11, 16, 17, 22, 23, 28, 29, 34, 35, 40, 41]:
        col_fdo = "V"
        
    return col_fdo


# Imagen de referencia victimas camara central
for indice in range(0, 42, 1):
    if indice <= 9:
        archivo = '../imagenes/IMG_Blanco/C_0' + str(
            indice) + '.jpg'
    else:
        archivo = '../imagenes/IMG_Blanco/C_' + str(
            indice) + '.jpg'
    image = imagen_ref(cv2.imread(archivo), encontrar_tipo(indice), "C", encontrar_color(indice), archivo)
    central_refference.append(image)  # imagen de referencia


# Imagen de referencia victima camara izquierda
for indice in range(0, 42, 1):
    if indice <= 9:
        archivo = '../imagenes/IMG_Blanco/I_0' + str(
            indice) + '.jpg'
    else:
        archivo = '../imagenes/IMG_Blanco/I_' + str(
            indice) + '.jpg'
    image = imagen_ref(cv2.imread(archivo), encontrar_tipo(indice), "L", encontrar_color(indice), archivo)
    left_refference.append(image)  # imagen de referencia

    
# Imagen de referencia victima camara derecha
for indice in range(0, 42, 1):
    if indice <= 9:
        archivo = '../imagenes/IMG_Blanco/D_0' + str(
            indice) + '.jpg'
    else:
        archivo = '../imagenes/IMG_Blanco/D_' + str(
            indice) + '.jpg'
    image = imagen_ref(cv2.imread(archivo), encontrar_tipo(indice), "R", (indice), archivo)
    right_refference.append(image)  # imagen de referenciaencontrar_color
# print(right_refference[7].getImagen())
# print(right_refference[7].getTipo())

indice = 0
dat_victima = victima("", 0, "", 0, 0)
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


def checkVic():
    global central_refference, left_refference, right_refference, indice, cam_enc
    arch_c = '../imagenes/cen/cen' + str(indice) + '.jpg'
    arch_l = '../imagenes/izq/izq' + str(indice) + '.jpg'
    arch_r = '../imagenes/der/der' + str(indice) + '.jpg'
    print(archivo)
    camera.saveImage(arch_c, 100)  # graba la imagen de la camara
    imag_c = cv2.imread(arch_c)  # imagen que ve el robot
    cameral.saveImage(arch_l, 100)  # graba la imagen de la camara
    imag_l = cv2.imread(arch_l)  # imagen que ve el robot
    camerar.saveImage(arch_r, 100)  # graba la imagen de la camara
    imag_r = cv2.imread(arch_r)  # imagen que ve el robot
    #indice = indice + 1
    posX = int(gps.getValues()[0] * 100)
    posZ = int(gps.getValues()[2] * 100)
    max_im = 0
    tip_im = ""
    reg_im = ""
    cam_im = ""
    col_im = ""
    cam_enc = ""
    for i in range(0, 42, 1):
        # print(i)
        resultado = cv2.matchTemplate(imag_c, central_refference[i].getImagen(), cv2.TM_CCOEFF_NORMED)
        min, max, pos_min, pos_max = cv2.minMaxLoc(resultado)
        # print('minimo ', min,' Maximo ', max,'Pos minimo ',pos_min,'Pos maximo ',pos_max)
        cam_im = central_refference[i].getCamara()
        col_im = central_refference[i].getColor()
        if (max > max_im and cam_im == "C" and col_im != "B"):
            max_im = max
            tip_im = central_refference[i].getTipo()
            cam_enc = "C"

    for i in range(0, 42, 1):
        resultado = cv2.matchTemplate(imag_l, left_refference[i].getImagen(), cv2.TM_CCOEFF_NORMED)
        min, max, pos_min, pos_max = cv2.minMaxLoc(resultado)
        # print('minimo ', min,' Maximo ', max,'Pos minimo ',pos_min,'Pos maximo ',pos_max)
        cam_im = left_refference[i].getCamara()
        col_im = left_refference[i].getColor()
        if (max > max_im and cam_im == "L" and col_im != "B"):
            max_im = max
            tip_im = left_refference[i].getTipo()
            cam_enc = "L"

    for i in range(0, 42, 1):
        resultado = cv2.matchTemplate(imag_r, right_refference[i].getImagen(), cv2.TM_CCOEFF_NORMED)
        min, max, pos_min, pos_max = cv2.minMaxLoc(resultado)
        # print('minimo ', min,' Maximo ', max,'Pos minimo ',pos_min,'Pos maximo ',pos_max)
        cam_im = right_refference[i].getCamara()
        col_im = right_refference[i].getColor()
        if (max > max_im and cam_im == "R" and col_im != "B"):
            max_im = max
            tip_im = right_refference[i].getTipo()
            cam_enc = "R"

    print('|maximo |', max_im, '| tipo |', tip_im, '| Camara |', cam_enc, '| Color |', col_im, '| archivo |', archivo)

    if (max_im > dat_victima.getValor()):
        dat_victima.setCamara(cam_im)
        dat_victima.setTipo(tip_im)
        dat_victima.setValor(max_im)
        dat_victima.setPosx(posX)
        dat_victima.setPosz(posZ)
    return max_im


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


def leer_camaras():
    global enc_victima
    global tipo_victima

    val_act = checkVic()
    val_ant = dat_victima.getValor()
    if (val_act < val_ant):
        if val_ant > 0.88:  ##0.69
            enc_victima  = dat_victima.getgetTipo()
            tipo_victima = enc_victima
        else:
            enc_victima  = ""
            tipo_victima = ""
            dat_victima.setCamara("")
            dat_victima.setPosx(0)
            dat_victima.setPosz(0)
            dat_victima.setTipo("")
            dat_victima.setValor(0)
    else:
        enc_victima  = ""
        tipo_victima = ""

    # print("victima ", enc_victima)


def inclinacionesVictim(cam):
    global inercia, contGVic, camG
    if contVic == 0:
        camG = cam

    if (camG == "L"):
        if (camG == "L" and l_ic == 0 and l_fi == 0):
            print("Opcion 1_L")
            inercia = "VIG"
            contGVic = 10
        elif (camG == "L" and l_ic == 0 and l_fi == 1):
            print("Opcion 2_L")
            inercia = "VI"
            contGVic = 50
        elif (camG == "L" and (l_id == 1 or l_fi == 1)):
            print("Opcion 3_L")
            inercia = "F"
            contGVic = 60

    elif (camG == "R"):
        if (camG == "R" and l_dc == 0 and l_fd == 0):
            print("Opcion 1_R")
            inercia = "VDG"
            contGVic = 10
        elif (camG == "D" and l_dc == 0 and l_fd == 1):
            print("Opcion 2_R")
            inercia = "VD"
            contGVic = 50
        elif (camG == "R" and (l_dd == 1 or l_fd == 1)):
            print("Opcion 3_R")
            inercia = "F"
            contGVic = 60

    elif (camG == "C"):
        if (camG == "C" and l_fd == 1 and l_fi == 1):
            print("Opcion 1_C")
            inercia = "VC"
            contGVic = 40
    else:
        inercia = "F"
        contGVic = 70
    print("entre a la inclinacion", inercia)



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