from robotDevices import *



def paro():
    print("-------- paro ------")
    ruedaDerecha.setVelocity(0)
    ruedaIzquierda.setVelocity(0)


# sigue de frente
def adelante():
    global inercia
    inercia = 'F'
    # print("adelante------")

    diferencia = d_delanteraIzquierda - d_centralizquierda
    # Si el robot esta centrado con ic
    if (diferencia >= 50 and diferencia <= 70):
        # y id es correcto seguimos de frente normal
        ruedaDerecha.setVelocity(speed_ordynary)
        ruedaIzquierda.setVelocity(speed_ordynary)
        print("sin ajuste")

    # Se alinea el robot si deteca paredes cercanas
    elif (d_delanteraIzquierda < 100 or d_centralizquierda < 100):
        print("me estoy alineando")

        if (diferencia < 50):
            ruedaDerecha.setVelocity(speed_ordynary)
            ruedaIzquierda.setVelocity(speed_max)
            # print("ajuste a la derecha")
        elif (diferencia > 70):
            ruedaDerecha.setVelocity(speed_max)
            ruedaIzquierda.setVelocity(speed_ordynary)
            # print("ajuste a la izquierda")


def salir():
    global inercia, count
    # print("salir ------", count)
    ruedaDerecha.setVelocity(speed_ordynary)
    ruedaIzquierda.setVelocity(speed_ordynary)
    count += (1 / pantano)


def entrar_izq():
    global inercia, count
    inercia = 'ez'
    # print("Terminar de salir ------", count)
    ruedaDerecha.setVelocity(speed_ordynary)
    ruedaIzquierda.setVelocity(speed_ordynary)
    count += (1 / pantano)


def entrar_der():
    global inercia, count
    inercia = 'ed'
    # print("Terminar de salir ------", count)
    ruedaDerecha.setVelocity(speed_ordynary)
    ruedaIzquierda.setVelocity(speed_ordynary)
    count += (1 / pantano)


def term_salir():
    global inercia, count
    inercia = 'TS'
    print("Terminar de salir ------", count)
    ruedaDerecha.setVelocity(speed_ordynary)
    ruedaIzquierda.setVelocity(speed_ordynary)
    count += (1 / pantano)


def izquierda():
    global count, inercia
    inercia = 'I'
    ruedaDerecha.setVelocity(speed_ordynary)
    ruedaIzquierda.setVelocity(speed_ordynary * -1)
    count += (1 / pantano)


def derecha():
    global count, inercia
    inercia = 'D'
    ruedaDerecha.setVelocity(speed_ordynary * -1)
    ruedaIzquierda.setVelocity(speed_ordynary)
    count = count + (1 / pantano)


# vuelta a la derecha
def giro_u():
    global inercia, inercia_ant, count, sigue, ts
    ts = 140
    inercia = "U"
    count += (1 / pantano)
    if (count <= tg):
        print("Inicia el Giro ", count, "tg ", tg)
        ruedaDerecha.setVelocity(speed_ordynary)
        ruedaIzquierda.setVelocity(speed_ordynary * -1)
    elif (d_frontalIzquierda >= d_frontalDerecha - 100 and count <= lg):
        print("Termina el giro ", count, "lg ", lg, "Diferencia ", d_frontalIzquierda-d_frontalDerecha)
        ruedaDerecha.setVelocity(speed_ordynary)
        ruedaIzquierda.setVelocity(speed_ordynary * -1)
    elif (count <= ts and inercia_ant != 'R'):
        print("Salir ", count," ts ", ts)
        ruedaDerecha.setVelocity(speed_ordynary)
        ruedaIzquierda.setVelocity(speed_ordynary)
    else:
        inercia_ant = 'U'
        inercia = "F"
        ts = 120
        adelante()


def sal_trampa():
    global step_c, inercia, ts, tg, lg, count
    # Retrocede
    ruedaDerecha.setVelocity(speed_max * -1)
    ruedaIzquierda.setVelocity(speed_max * -1)
    if (inercia != 'R'):
        count = 0

    inercia = "R"
    count += (1 / pantano)
    # print("Sailr de trampa  ", count," Pasos ",step_c)
    if count > 15:
        count = 0
        inercia = "U"


def alinear_izquierda():
    # print("alinear a la izquierda")
    ruedaDerecha.setVelocity(speed_ordynary)
    ruedaIzquierda.setVelocity(speed_ordynary * -1)


def alinear_derecha():
    # print("alinear a la derecha")
    ruedaDerecha.setVelocity(speed_ordynary * -1)
    ruedaIzquierda.setVelocity(speed_ordynary)


def ajustar():
    ajustar = False
    if (d_frontalDerecha != 0):
        multiplo = d_frontalIzquierda / d_frontalDerecha
        if (
            multiplo < 0.8
            and d_frontalIzquierda   > 500
            and d_frontalDerecha     < 500
            and l_centralIzquierdo    == 1
            and l_delanteroIzquierdo  == 1
            and l_centralDerecho      == 1
            and l_delanteroDerecho    == 1
        ):
            paro()
            print("Estoy pedrido me alineo a la izquierda",multiplo)
            alinear_izquierda()
            ajustar = True

        elif(
            multiplo > 1.2
            and d_frontalIzquierda   > 500
            and d_frontalDerecha     < 500
            and l_centralIzquierdo    == 1
            and l_delanteroIzquierdo  == 1
            and l_centralDerecho      == 1
            and l_delanteroDerecho    == 1
        ):
            paro()
            print("Estoy perdido me alineo a la derecha",multiplo)
            alinear_derecha()
            ajustar = True
    return ajustar


def direccion():
    global inercia, inercia_ant, sigue, step_c, count
    ins = 2
    print("--------------",inercia, "anterior ", inercia_ant)
    print(l_frontalDerecho,l_frontalIzquierdo)
    ## no hay paredes al frente
    if (inercia == 'F'):
        if (ajustar() == False):
            # no hay pared al frente y hay pared a la izquierda
            if (
                l_frontalDerecho == 1
                and l_frontalIzquierdo == 1
                and (l_delanteroIzquierdo == 0 or l_centralIzquierdo == 0)
            ):
                adelante()
            elif ((l_frontalDerecho == 0 and l_frontalIzquierdo == 0) and (l_centralDerecho == 1 or l_delanteroDerecho==1)):
                step_c = 40
                count = 0
                entrar_der()
            # Hay pared al frente y no hay pared a la izquierda(or o and)
            elif ((l_frontalDerecho == 0 and l_frontalIzquierdo == 0) and (l_delanteroIzquierdo == 1 or l_centralIzquierdo == 1)):
                step_c = 40
                count = 0
                entrar_izq()
            # No hay pared al frente y no hay pared a la izquierda
            elif ((l_frontalDerecho == 1 and l_frontalIzquierdo == 1) and (l_delanteroIzquierdo == 1 or l_centralIzquierdo == 1)):
                if (inercia_ant == 'U'):
                    step_c = 40
                    count = 0
                    entrar_izq()
                else:
                    step_c = 50
                    count = 0
                    inercia = 'SI'
                    salir()
            elif (l_frontalDerecho == 0 and l_frontalIzquierdo == 0 and l_delanteroIzquierdo == 0 and l_centralIzquierdo == 0 and l_delanteroDerecho == 0 and l_centralDerecho == 0):
                step_c = 35
                count = 0
                giro_u()
            else:
                adelante()
    elif inercia == 'ez':
        print('entrando ala izquierda', count)
        entrar_izq()
        if count>step_c:
            inercia_ant='ez'
            step_c = 35
            count = 0
            izquierda()
    elif inercia == 'ed':
        print('entrando ala derecha', count)
        entrar_der()
        if count>step_c:
            inercia_ant= 'ed'
            step_c = 35
            count = 0
            derecha()
    elif inercia == 'S':
        salir()
        # print("Salir", count)
        if (count > step_c or l_frontalDerecho == 0 or l_frontalIzquierdo == 0):
            inercia_ant = 'S'
            inercia = "F"
            adelante()
    elif inercia == 'D':
        derecha()
        # print("Derecha", count)
        if (count > step_c):
            inercia_ant = 'D'
            step_c = 40
            count = 0
            term_salir()
    elif inercia == 'I':
        # print("aqui")
        izquierda()
        print("Izquierda", count)
        if (count > step_c):
            inercia_ant = 'I'
            step_c = 40
            count = 0
            term_salir()
    elif inercia == 'SI':
        inercia_ant = 'SI'
        if (count < step_c):
            salir()
        else:
            step_c = 35
            count = 0
            izquierda()
    elif inercia == "R":
        inercia_ant = 'R'
        sal_trampa()
    elif inercia == "DT":
        derecha()
        # print("Salir de derecha trampa", count)
        if (count > step_c):
            inercia_ant = 'DT'
            step_c = 40
            count = 0
            term_salir()
    elif inercia == "IT":
        izquierda()
        # print("Salir de izquierda trampa", count)
        if (count > step_c):
            inercia_ant = 'IT'
            step_c = 40
            count = 0
            term_salir()
    elif inercia == "TS":
        term_salir()
        # print("Terminar de salir", count)
        if (count > step_c or l_frontalDerecho == 0 or l_frontalIzquierdo == 0):
            inercia_ant = 'TS'
            step_c = 0
            count = 0
            adelante()
    elif inercia == 'U':
        print("U")
        giro_u()
    elif inercia == "VI":
        print("acercar a victima_L")
        ruedaDerecha.setVelocity(speed_ordynary)
        ruedaIzquierda.setVelocity(speed_baj)
    elif inercia == "VD":
        print("acercar a victima_R")
        ruedaIzquierda.setVelocity(speed_ordynary)
        ruedaDerecha.setVelocity(speed_baj)
    elif inercia == "VIG":
        ruedaDerecha.setVelocity(speed_max)
        ruedaIzquierda.setVelocity(speed_baj)
    elif inercia == "VDG":
        ruedaIzquierda.setVelocity(speed_max)
        ruedaDerecha.setVelocity(speed_baj)
    elif inercia == "VC":
        ruedaIzquierda.setVelocity(speed_ordynary)
        ruedaDerecha.setVelocity(speed_ordynary)