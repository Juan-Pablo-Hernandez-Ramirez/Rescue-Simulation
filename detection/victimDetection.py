import cv2
from sys import path




path.append("../detection")
from victimDetection import *

path.append("../classes")
from c_imagen  import imagen_ref
from c_victima import victima

path.append("../functions")
from robotDevices import *
 

left_refference    = []
central_refference = []
right_refference   = []

dat_victima = victima("", 0, "", 0, 0)


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




