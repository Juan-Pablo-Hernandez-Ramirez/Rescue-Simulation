class victima:
    ## definicion de las propiedades de la clase y asignación de valores por omisión
    def __init__(self, ti, va, ca, px, pz):
        self.tipo = ti
        self.valor = va
        self.camara = ca
        self.posx = px
        self.posz = pz

    ## Definición de metodos de asignación para las propiedades de la clase
    def setTipo(self, ti):
        self.tipo = ti

    def setValor(self, va):
        self.valor = va

    def setCamara(self, ca):
        self.camara = ca

    def setPosx(self, px):
        self.posx = px

    def setPosz(self, pz):
        self.posz = pz

    ##definción del metodo que ejecuta la operación y guarda la operación y resultado a la memoria
    def getgetTipo(self):
        return self.tipo

    def getValor(self):
        return self.valor

    def getCamara(self):
        return self.camara

    def getPosx(self):
        return self.posx

    def getPosz(self):
        return self.posz
