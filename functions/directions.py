from robotDevices import *



def paro():
    print("-------- paro ------")
    rueda_rdf.setVelocity(0)
    rueda_rif.setVelocity(0)


# sigue de frente
def adelante():
    global inercia
    inercia = 'F'
    # print("adelante------")

    diferencia = d_id - d_ic
    # Si el robot esta centrado con ic
    if (diferencia >= 50 and diferencia <= 70):
        # y id es correcto seguimos de frente normal
        rueda_rdf.setVelocity(speed_ordynary)
        rueda_rif.setVelocity(speed_ordynary)
        # print("sin ajuste")
    elif (diferencia < 50):
        rueda_rdf.setVelocity(speed_ordynary)
        rueda_rif.setVelocity(speed_max)
        # print("ajuste a la derecha")
    elif (diferencia > 70):
        rueda_rdf.setVelocity(speed_max)
        rueda_rif.setVelocity(speed_ordynary)
        # print("ajuste a la izquierda")


def salir():
    global inercia
    global count
    # print("salir ------", count)
    rueda_rdf.setVelocity(speed_ordynary)
    rueda_rif.setVelocity(speed_ordynary)
    count = count + (1 / pantano)


def entrar_izq():
    global inercia
    global count
    inercia = 'ez'
    # print("Terminar de salir ------", count)
    rueda_rdf.setVelocity(speed_ordynary)
    rueda_rif.setVelocity(speed_ordynary)
    count = count + (1 / pantano)


def entrar_der():
    global inercia
    global count
    inercia = 'ed'
    # print("Terminar de salir ------", count)
    rueda_rdf.setVelocity(speed_ordynary)
    rueda_rif.setVelocity(speed_ordynary)
    count = count + (1 / pantano)


def term_salir():
    global inercia
    global count
    inercia = 'TS'
    # print("Terminar de salir ------", count)
    rueda_rdf.setVelocity(speed_ordynary)
    rueda_rif.setVelocity(speed_ordynary)
    count = count + (1 / pantano)


def izquierda():
    global count
    global inercia
    inercia = 'I'
    rueda_rdf.setVelocity(speed_ordynary)
    rueda_rif.setVelocity(speed_ordynary * -1)
    count = count + (1 / pantano)


def derecha():
    global count
    global inercia
    inercia = 'D'
    rueda_rdf.setVelocity(speed_ordynary * -1)
    rueda_rif.setVelocity(speed_ordynary)
    count = count + (1 / pantano)


# vuelta a la derecha
def giro_u():
    global inercia
    global inercia_ant
    global count
    global sigue
    global termina
    global ts
    ts = 140
    inercia = "U"
    count = count + (1 / pantano)
    if (count <= tg):
        print("Inicia el Giro ", count, "tg ", tg)
        rueda_rdf.setVelocity(speed_ordynary)
        rueda_rif.setVelocity(speed_ordynary * -1)
    elif (d_fi >= d_fd - 100 and count <= lg):
        print("Termina el giro ", count, "lg ", lg, "Diferencia ", d_fi-d_fd)
        rueda_rdf.setVelocity(speed_ordynary)
        rueda_rif.setVelocity(speed_ordynary * -1)
    elif (count <= ts and inercia_ant != 'R'):
        print("Salir ", count," ts ", ts)
        rueda_rdf.setVelocity(speed_ordynary)
        rueda_rif.setVelocity(speed_ordynary)
    else:
        inercia_ant = 'U'
        inercia = "F"
        ts = 120
        adelante()


def sal_trampa():
    global step_c
    global inercia
    global ts
    global tg
    global lg
    global count
    # Retrocede
    rueda_rdf.setVelocity(speed_max * -1)
    rueda_rif.setVelocity(speed_max * -1)
    if (inercia != 'R'):
        count = 0
    inercia = "R"
    count = count + (1 / pantano)
    # print("Sailr de trampa  ", count," Pasos ",step_c)
    if count > 15:
        count = 0
        inercia = "U"


def alinear_izquierda():
    # print("alinear a la izquierda")
    rueda_rdf.setVelocity(speed_ordynary)
    rueda_rif.setVelocity(speed_ordynary * -1)


def alinear_derecha():
    # print("alinear a la derecha")
    rueda_rdf.setVelocity(speed_ordynary * -1)
    rueda_rif.setVelocity(speed_ordynary)


def ajustar():
    ajustar = False
    if (d_fd != 0):
        multiplo = d_fi / d_fd
        if (multiplo < 0.8 and l_fi == 1 and l_fd == 1 and l_ic == 1 and l_id == 1 and l_dc == 1 and l_dd == 1):
            # paro()
            print("Estoy pedrido me alineo a la izquierda",multiplo)
            alinear_izquierda()
            ajustar = True
        elif (multiplo > 1.2 and l_fi == 1 and l_fd == 1 and l_ic == 1 and l_id == 1 and l_dc == 1 and l_dd == 1):
            # paro()
            print("Estoy perdido me alineo a la derecha",multiplo)
            alinear_izquierda()
            # alinear_derecha()
            ajustar = True
    return ajustar


def direccion():
    global inercia
    global inercia_ant
    global sigue
    global step_c
    global count
    ins = 2
    print("--------------",inercia, "anterior ", inercia_ant)
    print(l_fd,l_fi)
    ## no hay paredes al frente
    if (inercia == 'F'):
        if (ajustar() == False):
            # no hay pared al frente y hay pared a la izquierda
            if (l_fd == 1 and l_fi == 1 and (l_id == 0 or l_ic == 0)):
                adelante()
            elif ((l_fd == 0 and l_fi == 0) and (l_dc == 1 or l_dd==1)):
                step_c = 40
                count = 0
                entrar_der()
            # Hay pared al frente y no hay pared a la izquierda(or o and)
            elif ((l_fd == 0 and l_fi == 0) and (l_id == 1 or l_ic == 1)):
                step_c = 40
                count = 0
                entrar_izq()
            # No hay pared al frente y no hay pared a la izquierda
            elif ((l_fd == 1 and l_fi == 1) and (l_id == 1 or l_ic == 1)):
                if (inercia_ant == 'U'):
                    step_c = 40
                    count = 0
                    entrar_izq()
                else:
                    step_c = 50
                    count = 0
                    inercia = 'SI'
                    salir()
            elif (l_fd == 0 and l_fi == 0 and l_id == 0 and l_ic == 0 and l_dd == 0 and l_dc == 0):
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
        if (count > step_c or l_fd == 0 or l_fi == 0):
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
        if (count > step_c or l_fd == 0 or l_fi == 0):
            inercia_ant = 'TS'
            step_c = 0
            count = 0
            adelante()
    elif inercia == 'U':
        print("U")
        giro_u()
    elif inercia == "VI":
        print("acercar a victima_L")
        rueda_rdf.setVelocity(speed_ordynary)
        rueda_rif.setVelocity(speed_baj)
    elif inercia == "VD":
        print("acercar a victima_R")
        rueda_rif.setVelocity(speed_ordynary)
        rueda_rdf.setVelocity(speed_baj)
    elif inercia == "VIG":
        rueda_rdf.setVelocity(speed_max)
        rueda_rif.setVelocity(speed_baj)
    elif inercia == "VDG":
        rueda_rif.setVelocity(speed_max)
        rueda_rdf.setVelocity(speed_baj)
    elif inercia == "VC":
        rueda_rif.setVelocity(speed_ordynary)
        rueda_rdf.setVelocity(speed_ordynary)