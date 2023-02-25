# Procedimiento de lectura de sensores de distancia
def lee_distancia():
    global d_frontalDerecha
    global d_frontalIzquierda
    global d_delanteraDerecha
    global d_centralDerecha
    global d_delanteraIzquierda
    global d_centralizquierda
    global l_frontalDerecho
    global l_frontalIzquierdo
    global l_delanteroDerecho
    global l_centralDerecho
    global l_delanteroIzquierdo
    global l_centralIzquierdo

    d_frontalDerecha = int(sensor_fd.getValue() * 1000)
    d_frontalIzquierda = int(sensor_fi.getValue() * 1000)
    d_delanteraDerecha = int(sensor_dd.getValue() * 1000)
    d_centralDerecha = int(sensor_dc.getValue() * 1000)
    d_delanteraIzquierda = int(sensor_id.getValue() * 1000)
    d_centralizquierda = int(sensor_ic.getValue() * 1000)

    if (d_centralizquierda > 500 and d_delanteraIzquierda < frente):
        print("estoy pagado a la pared izquierda")
        d_centralizquierda = 0

    if (d_centralDerecha > 500 and d_delanteraDerecha < frente):
        print("estoy pagado a la pared derecha")
        d_centralDerecha = 0

    '''if (d_frontalDerecha>600 and d_frontalIzquierda>600 and (d_delanteraDerecha<frente or d_delanteraIzquierda<frente)):
        print("estoy pagado a la pared frontal a la derecha")
        d_frontalDerecha=0
        d_frontalIzquierda=0'''

    if (d_frontalDerecha > 600 and d_delanteraDerecha < frente):
        print("estoy pagado a la pared frontal a la derecha")
        d_frontalDerecha = 0

    if (d_frontalIzquierda > 600 and d_delanteraIzquierda < frente):
        print("estoy pagado a la pared frontal a la izquierda")
        d_frontalIzquierda = 0

    ## logicos al frente
    if (d_frontalDerecha > frente):
        l_frontalDerecho = 1  ## no hay pared al frente
    else:
        l_frontalDerecho = 0  ## hay pared al frente

    if (d_frontalIzquierda > frente):
        l_frontalIzquierdo = 1  ## no hay pared al frente
    else:
        l_frontalIzquierdo = 0  ## hay pared al frente

    ## logicos a las paredes
    if (d_delanteraDerecha > muros):
        l_delanteroDerecho = 1  ## no hay pared a la derecha
    else:
        l_delanteroDerecho = 0  ## hay pared a la derecha

    if (d_centralDerecha > muros):
        l_centralDerecho = 1  ## no hay pared a la derecha
    else:
        l_centralDerecho = 0  ## hay pared a la derecha

    if (d_delanteraIzquierda > muros):
        l_delanteroIzquierdo = 1  ## no hay pared a la izquierda
    else:
        l_delanteroIzquierdo = 0  ## hay pared a la izquierda

    if (d_centralizquierda > muros):
        l_centralIzquierdo = 1  ## no hay pared a la izquierda
    else:
        l_centralIzquierdo = 0  ## hay pared a la izquierda

    # print('distancia fd ', d_frontalDerecha,'  fi ', d_frontalIzquierda,' derecha delantero ',d_delanteraDerecha,' derecha central ',d_centralDerecha," izquierda delantero ",d_delanteraIzquierda," izquierda central ",d_centralizquierda)
    print('logica fd ', l_frontalDerecho,'  fi ', l_frontalIzquierdo,' derecha delantero ',l_delanteroDerecho,' derecha central ',l_centralDerecho," izquierda delantero ",l_delanteroIzquierdo," izquierda central ",l_centralIzquierdo)
