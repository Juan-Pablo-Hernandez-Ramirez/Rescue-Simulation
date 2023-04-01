import cv2
from sys import path


path.append("../detection")
from victimDetection import *

path.append("../classes")
from c_imagen  import imagen_ref
from c_victima import victima

path.append("../functions")
from robotDevices import *
 
referencia_victimas  = []
referencia_izquierda = []
referencia_central   = []
referencia_derecha   = []

dat_victima = victima("", 0, "", 0, 0)


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
            dat_victima.setPosX(0)
            dat_victima.setPosZ(0)
            dat_victima.setTipo("")
            dat_victima.setValor(0)
    else:
        enc_victima  = ""
        tipo_victima = ""

    # print("victima ", enc_victima)


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

victimaEncontrada = ""

def checkVic():
    global referencia_victimas, referencia_central, referencia_izquierda, referencia_derecha, indice, cam_enc, victimaEncontrada
    archivoCentral   = '../imagenes/cen/cen' + str(indice) + '.jpg'
    archivoIzquierdo = '../imagenes/izq/izq' + str(indice) + '.jpg'
    archivoDerecho   = '../imagenes/der/der' + str(indice) + '.jpg'

    camaraCentral.saveImage(archivoCentral, 100)  # graba la imagen de la camara
    imagenCentral = cv2.imread(archivoCentral)  # imagen que ve el 


    camaraIzquierda.saveImage(archivoIzquierdo, 100)  # graba la imagen de la camara
    imagenIzquierda = cv2.imread(archivoIzquierdo)  # imagen que ve el robot

    camaraDerecha.saveImage(archivoDerecho, 100)  # graba la imagen de la camara
    imagenDerecha = cv2.imread(archivoDerecho)  # imagen que ve el robot
    #indice = indice + 1
    posX = int(gps.getValues()[0] * 100)
    posZ = int(gps.getValues()[2] * 100)
    max_im = 0
    tip_im = ""
    reg_im = ""
    cam_im = ""
    col_im = ""
    cam_enc = ""
    

    for i in range(0, 3, 1):
        # print(i)
        resultado = cv2.matchTemplate(imagenCentral, referencia_victimas[i].getImagen(), cv2.TM_CCOEFF_NORMED)
        min, max, pos_min, pos_max = cv2.minMaxLoc(resultado)
        print(max)
        cam_im = referencia_victimas[i].getCamara()
        col_im = referencia_victimas[i].getColor()


        print("---------- central, max:", max, "max_im:", max_im, "cam_im", cam_im, "col_im", col_im, "----------")

        if (max > max_im and cam_im == "V" and col_im != "B"):
            victimaEncontrada = "CC"
            max_im = max
            tip_im = referencia_central[i].getTipo()
            cam_enc = "C"

        resultado = cv2.matchTemplate(imagenIzquierda, referencia_victimas[i].getImagen(), cv2.TM_CCOEFF_NORMED)
        min, max, pos_min, pos_max = cv2.minMaxLoc(resultado)
        cam_im = referencia_victimas[i].getCamara()
        col_im = referencia_victimas[i].getColor()
        if (max > max_im and cam_im == "V" and col_im != "B"):
            victimaEncontrada = "CI"
            max_im = max
            tip_im = referencia_izquierda[i].getTipo()
            cam_enc = "L"

        resultado = cv2.matchTemplate(imagenDerecha, referencia_victimas[i].getImagen(), cv2.TM_CCOEFF_NORMED)
        min, max, pos_min, pos_max = cv2.minMaxLoc(resultado)
        cam_im = referencia_victimas[i].getCamara()
        col_im = referencia_victimas[i].getColor()
        if (max > max_im and cam_im == "V" and col_im != "B"):
            victimaEncontrada = "CD"
            max_im = max
            tip_im = referencia_derecha[i].getTipo()
            cam_enc = "R"


        if (victimaEncontrada == "CC"):
            print("--------------- SE ENTRO A LA CONDICION ---------------")
            for i in range(0, 20, 1):
                # print(i)
                resultado = cv2.matchTemplate(imagenCentral, referencia_central[i].getImagen(), cv2.TM_CCOEFF_NORMED)
                min, max, pos_min, pos_max = cv2.minMaxLoc(resultado)
                # print('minimo ', min,' Maximo ', max,'Pos minimo ',pos_min,'Pos maximo ',pos_max)
                cam_im = referencia_central[i].getCamara()
                col_im = referencia_central[i].getColor()
                if (max > max_im and cam_im == "C" and col_im != "B"):
                    max_im = max
                    tip_im = referencia_central[i].getTipo()
                    cam_enc = "C"

        print("------------ ERROR ------------")


        if (victimaEncontrada == "CI"):
            print("--------------- SE ENTRO A LA CONDICION 2 ---------------")
            for i in range(0, 20, 1):
                resultado = cv2.matchTemplate(imagenIzquierda, referencia_izquierda[i].getImagen(), cv2.TM_CCOEFF_NORMED)
                min, max, pos_min, pos_max = cv2.minMaxLoc(resultado)
                # print('minimo ', min,' Maximo ', max,'Pos minimo ',pos_min,'Pos maximo ',pos_max)
                cam_im = referencia_izquierda[i].getCamara()
                col_im = referencia_izquierda[i].getColor()
                if (max > max_im and cam_im == "L" and col_im != "B"):
                    max_im = max
                    tip_im = referencia_izquierda[i].getTipo()
                    cam_enc = "L"

        elif (victimaEncontrada == "CD"):
            print("--------------- SE ENTRO A LA CONDICION 3 ---------------")
            for i in range(0, 20, 1):
                resultado = cv2.matchTemplate(imagenDerecha, referencia_derecha[i].getImagen(), cv2.TM_CCOEFF_NORMED)
                min, max, pos_min, pos_max = cv2.minMaxLoc(resultado)
                # print('minimo ', min,' Maximo ', max,'Pos minimo ',pos_min,'Pos maximo ',pos_max)
                cam_im = referencia_derecha[i].getCamara()
                col_im = referencia_derecha[i].getColor()
                if (max > max_im and cam_im == "R" and col_im != "B"):
                    max_im = max
                    tip_im = referencia_derecha[i].getTipo()
                    cam_enc = "R"

        else:
            print("--------------- NO SE ENCONTRO NINGUNA VICTIMA ---------------")








        print('|maximo |', max_im, '| tipo |', tip_im, '| Camara |', cam_enc, '| Color |', col_im, '| archivo |', archivo)

        if (max_im > dat_victima.getValor()):
            dat_victima.setCamara(cam_im)
            dat_victima.setTipo(tip_im)
            dat_victima.setValor(max_im)
            dat_victima.setPosX(posX)
            dat_victima.setPosZ(posZ)
        return max_im


def inclinacionesVictim(cam):
    global inercia, contGVic, camG
    if contVic == 0:
        camG = cam

    if (camG == "L"):
        if (camG == "L" and l_centralIzquierdo == 0 and l_frontalIzquierdo == 0):
            print("Opcion 1_L")
            inercia = "VIG"
            contGVic = 10
        elif (camG == "L" and l_centralIzquierdo == 0 and l_frontalIzquierdo == 1):
            print("Opcion 2_L")
            inercia = "VI"
            contGVic = 50
        elif (camG == "L" and (l_delanteroIzquierdo == 1 or l_frontalIzquierdo == 1)):
            print("Opcion 3_L")
            inercia = "F"
            contGVic = 60

    elif (camG == "R"):
        if (camG == "R" and l_centralDerecho == 0 and l_frontalDerecho == 0):
            print("Opcion 1_R")
            inercia = "VDG"
            contGVic = 10
        elif (camG == "D" and l_centralDerecho == 0 and l_frontalDerecho == 1):
            print("Opcion 2_R")
            inercia = "VD"
            contGVic = 50
        elif (camG == "R" and (l_delanteroDerecho == 1 or l_frontalDerecho == 1)):
            print("Opcion 3_R")
            inercia = "F"
            contGVic = 60

    elif (camG == "C"):
        if (camG == "C" and l_frontalDerecho == 1 and l_frontalIzquierdo == 1):
            print("Opcion 1_C")
            inercia = "VC"
            contGVic = 40
    else:
        inercia = "F"
        contGVic = 70
    print("entre a la inclinacion", inercia)


def encontrarColor(ind):
# -------------- H  H, S  S,  U   U,  C   C,  P   P,  F   F,  O,  O  #
    if   ind in [0, 1, 6, 7, 12, 13, 18, 19, 24, 25, 30, 31, 36, 37]:
        colorFondo = "B"

# -------------- H  H, S  S,  U   U,  C   C,  P   P,  F   F,  O,  O  #
    elif ind in [2, 3, 8, 9, 14, 15, 20, 21, 26, 27, 32, 33, 38, 39]:
        colorFondo = "N"
        
# -------------- H  H, S   S,  U   U,  C   C,  P   P,  F   F,  O,  O  #
    elif ind in [4, 5, 10, 11, 16, 17, 22, 23, 28, 29, 34, 35, 40, 41]:
        colorFondo = "V"
        
    return colorFondo


# ------------------------- Busqueda de victimas visuales ------------------------- #

# Imagen de referencia victimas camara central
for indice in range(0, 3, 1):
    
    archivo = '../imagenes/victimasDistancia/victima_d' + str(
            indice) + '.jpg'

    image = imagen_ref(cv2.imread(archivo), encontrar_tipo(indice), "V", encontrarColor(indice), archivo)
    referencia_victimas.append(image)  # imagen de referencia


# Imagen de referencia victimas camara central
for indice in range(0, 42, 1):
    if indice <= 9:
        archivo = '../imagenes/IMG_Blanco/C_0' + str(
            indice) + '.jpg'
    else:
        archivo = '../imagenes/IMG_Blanco/C_' + str(
            indice) + '.jpg'
    image = imagen_ref(cv2.imread(archivo), encontrar_tipo(indice), "C", encontrarColor(indice), archivo)
    referencia_central.append(image)  # imagen de referencia



# Imagen de referencia victima camara izquierda
for indice in range(0, 42, 1):
    if indice <= 9:
        archivo = '../imagenes/IMG_Blanco/I_0' + str(
            indice) + '.jpg'
    else:
        archivo = '../imagenes/IMG_Blanco/I_' + str(
            indice) + '.jpg'
    image = imagen_ref(cv2.imread(archivo), encontrar_tipo(indice), "L", encontrarColor(indice), archivo)
    referencia_izquierda.append(image)  # imagen de referencia


# Imagen de referencia victima camara derecha
for indice in range(0, 42, 1):
    if indice <= 9:
        archivo = '../imagenes/IMG_Blanco/D_0' + str(
            indice) + '.jpg'
    else:
        archivo = '../imagenes/IMG_Blanco/D_' + str(
            indice) + '.jpg'
    image = imagen_ref(cv2.imread(archivo), encontrar_tipo(indice), "R", (indice), archivo)
    referencia_derecha.append(image)  # imagen de referenciaencontrarColor
# print(referencia_derecha[7].getImagen())
# print(referencia_derecha[7].getTipo())
